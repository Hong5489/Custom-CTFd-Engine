from flask import session, request, abort, url_for
from flask_restx import Namespace, Resource
from CTFd.models import (
	db,
	Challenges,
	Unlocks,
	HintUnlocks,
	Tags,
	Hints,
	Flags,
	Solves,
	Submissions,
	Fails,
	ChallengeFiles as ChallengeFilesModel,
	Ports,
	Category,
	Writeups,
	Users,
	Likes,
)
from CTFd.plugins.challenges import get_chal_class, CHALLENGE_CLASSES
from CTFd.utils.dates import ctf_ended, isoformat
from CTFd.utils.decorators import (
	during_ctf_time_only,
	require_verified_emails,
	admins_only,
	authed_only
)
from CTFd.utils.decorators.visibility import (
	check_challenge_visibility,
	check_score_visibility
)
from CTFd.cache import cache, clear_standings
from CTFd.utils.scores import get_standings
from CTFd.utils.config.visibility import scores_visible, accounts_visible, challenges_visible
from CTFd.utils.user import get_current_user, is_admin, authed
from CTFd.utils.modes import get_model, USERS_MODE, TEAMS_MODE
from CTFd.schemas.tags import TagSchema
from CTFd.schemas.hints import HintSchema
from CTFd.schemas.flags import FlagSchema
from CTFd.utils import config, get_config
from CTFd.utils import user as current_user
from CTFd.utils.user import get_current_team
from CTFd.utils.user import get_current_user
from CTFd.plugins.challenges import get_chal_class
from CTFd.utils.dates import ctf_started, ctf_ended, ctf_paused, ctftime
from CTFd.utils.logging import log
from sqlalchemy.sql import or_, and_, any_

challenges_namespace = Namespace('challenges',
								 description="Endpoint to retrieve Challenges")


@challenges_namespace.route('')
class ChallengeList(Resource):
	@check_challenge_visibility
	@during_ctf_time_only
	@require_verified_emails
	def get(self):
		# This can return None (unauth) if visibility is set to public
		user = get_current_user()

		challenges = Challenges.query.filter(
			and_(Challenges.state != 'hidden', Challenges.state != 'locked')
		).order_by(Challenges.difficulty).all()

		if user:
			solve_ids = Solves.query\
				.with_entities(Solves.challenge_id)\
				.filter_by(account_id=user.account_id)\
				.order_by(Solves.challenge_id.asc())\
				.all()
			solve_ids = set([value for value, in solve_ids])
		else:
			solve_ids = set()

		response = []
		tag_schema = TagSchema(view='user', many=True)
		from fyp import selectCategory
		for challenge in challenges:
			challenge_type = get_chal_class(challenge.type)
			if challenge.requirements:
				requirements = challenge.requirements.get('prerequisites', [])
				anonymize = challenge.requirements.get('anonymize')
				prereqs = set(requirements)
				if solve_ids >= prereqs:
					pass
				else:
					response.append({
						'id': challenge.id,
						'type': challenge_type.name,
						'name': challenge.name,
						'value': challenge.value,
						# 'category': challenge.category,
						'category_id': challenge.category_id,
						'tags': tag_schema.dump(challenge.tags).data,
						'template': challenge_type.templates['view'],
						'script': challenge_type.scripts['view'],
						'lock':True,
			'requirement': [Challenges.query.filter(Challenges.id == p).first().name for p in list(prereqs) if Challenges.query.filter(Challenges.id == p).first()]
					})
					continue
			#         pass
			#     else:
			#         if anonymize:
			#             response.append({
			#                 'id': challenge.id,
			#                 'type': 'hidden',
			#                 'name': '???',
			#                 'value': 0,
			#                 'category': '???',
			#                 'tags': [],
			#                 'template': '',
			#                 'script': ''
			#             })
			#         # Fallthrough to continue
			#         continue
			response.append({
				'id': challenge.id,
				'type': challenge_type.name,
				'name': challenge.name,
				'value': challenge.value,
				# 'category': challenge.category,
				'category_id': challenge.category_id,
				'tags': tag_schema.dump(challenge.tags).data,
				'template': challenge_type.templates['view'],
				'script': challenge_type.scripts['view'],
				'lock':False,
			})


		db.session.close()
		return {
			'success': True,
			'data': response
		}

	@admins_only
	def post(self):
		data = request.form or request.get_json()
		challenge_type = data['type']
		challenge_class = get_chal_class(challenge_type)
		challenge = challenge_class.create(request)
		response = challenge_class.read(challenge)
		return {
			'success': True,
			'data': response
		}


@challenges_namespace.route('/types')
class ChallengeTypes(Resource):
	@admins_only
	def get(self):
		response = {}

		for class_id in CHALLENGE_CLASSES:
			challenge_class = CHALLENGE_CLASSES.get(class_id)
			response[challenge_class.id] = {
				'id': challenge_class.id,
				'name': challenge_class.name,
				'templates': challenge_class.templates,
				'scripts': challenge_class.scripts,
			}
		return {
			'success': True,
			'data': response
		}


@challenges_namespace.route('/<challenge_id>')
@challenges_namespace.param('challenge_id', 'A Challenge ID')
class Challenge(Resource):
	@check_challenge_visibility
	@during_ctf_time_only
	@require_verified_emails
	def get(self, challenge_id):
		if is_admin():
			chal = Challenges.query.filter(Challenges.id == challenge_id).first_or_404()
		else:
			chal = Challenges.query.filter(
				Challenges.id == challenge_id, and_(Challenges.state != 'hidden', Challenges.state != 'locked')
			).first_or_404()

		chal_class = get_chal_class(chal.type)

		if chal.requirements:
			requirements = chal.requirements.get('prerequisites', [])
			anonymize = chal.requirements.get('anonymize')
			if challenges_visible():
				user = get_current_user()
				if user:
					solve_ids = Solves.query \
						.with_entities(Solves.challenge_id) \
						.filter_by(account_id=user.account_id) \
						.order_by(Solves.challenge_id.asc()) \
						.all()
				else:
					# We need to handle the case where a user is viewing challenges anonymously
					solve_ids = []
				solve_ids = set([value for value, in solve_ids])
				prereqs = set(requirements)
				if solve_ids >= prereqs or is_admin():
					pass
				else:
					if anonymize:
						return {
							'success': True,
							'data': {
								'id': chal.id,
								'type': 'hidden',
								'name': '???',
								'value': 0,
								'category': '???',
								'tags': [],
								'template': '',
								'script': ''
							}
						}
					abort(403)
			else:
				abort(403)

		tags = [
			tag['value'] for tag in TagSchema(
				"user", many=True).dump(
				chal.tags).data]
		files = [f.location for f in chal.files]

		unlocked_hints = set()
		hints = []
		if authed():
			user = get_current_user()
			unlocked_hints = set([u.target for u in HintUnlocks.query.filter_by(
				type='hints', account_id=user.account_id)])

		for hint in Hints.query.filter_by(challenge_id=chal.id).all():
			if hint.id in unlocked_hints or ctf_ended():
				hints.append({'id': hint.id, 'cost': hint.cost,
							  'content': hint.content})
			else:
				hints.append({'id': hint.id, 'cost': hint.cost})

		response = chal_class.read(challenge=chal)

		Model = get_model()

		if scores_visible() is True and accounts_visible() is True:
			solves = Solves.query\
				.join(Model, Solves.account_id == Model.id)\
				.filter(Solves.challenge_id == chal.id, Model.banned == False, Model.hidden == False)\
				.count()
			response['solves'] = solves
		else:
			response['solves'] = None

		response['files'] = files
		response['tags'] = tags
		response['hints'] = hints
		if chal.type == "web":
			if chal.ports:
				for p in chal.ports:
					if p.team_id == get_current_team().id:
						response['ports'] = p.url
						break

		db.session.close()
		return {
			'success': True,
			'data': response
		}

	@admins_only
	def patch(self, challenge_id):
		challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()
		challenge_class = get_chal_class(challenge.type)
		challenge = challenge_class.update(challenge, request)
		response = challenge_class.read(challenge)
		return {
			'success': True,
			'data': response
		}

	@admins_only
	def delete(self, challenge_id):
		challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()
		chal_class = get_chal_class(challenge.type)
		chal_class.delete(challenge)

		return {
			'success': True,
		}
@challenges_namespace.route('/ports')
class ChallengeManagePorts(Resource):
	@during_ctf_time_only
	@require_verified_emails
	def post(self):
		if authed() is False:
			return {
				'success': True,
				'data': {
					'status': "authentication_required",
				}
			}, 403

		if request.content_type != 'application/json':
			request_data = request.form
		else:
			request_data = request.get_json()
		close = request.args.get('close', False)

		challenge_id = request_data.get('challenge_id')
		challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()
		team = get_current_team()
		port = Ports.query.filter_by(challenge_id=challenge_id,team_id=team.id).first()

		if close:
			if port == None:
				return {
					'success': True,
					'data': {
						'status': "incorrect",
						'message': "Another member closed / Over time limit"
					}
				}
			db.session.delete(port)
			db.session.commit()
			from fyp import closePort
			closePort(port.url)
			return {
				'success': True,
				'data': {
					'status': "already_solved",
					'message': "Successfully closed port"
				}
			}
		if port:
			return {
				'success': True,
				'data': {
					'status': "incorrect",
					'message': "Another member already opened"
				}
			}
		ports_id = [i[0] for i in db.session.query(Ports.number)]
		target_port = 4000
		while target_port in ports_id:
			target_port += 1
		if target_port > 4005:
			return {
				'success': True,
				'data': {
					'status': "incorrect",
					'message': "Insufficient ports to open, wait or close opened port"
				}
			}
		port = Ports(
			number = target_port
		)
		db.session.add(port)
		port.team_id = team.id
		port.challenge_id = challenge_id
		from os import urandom
		port.url = urandom(16).hex()
		db.session.commit()
		flag = Flags.query.filter_by(challenge_id=challenge.id).first_or_404()
		from fyp import createPort
		createPort(challenge,flag.content,team,port)
		return {
			'success': True,
			'data': {
				'status': "already_solved",
				'message': "Successfully created port",
				'url': port.url
			}
		}

@challenges_namespace.route('/attempt')
class ChallengeAttempt(Resource):
	@during_ctf_time_only
	@require_verified_emails
	def post(self):
		if authed() is False:
			return {
				'success': True,
				'data': {
					'status': "authentication_required",
				}
			}, 403

		if request.content_type != 'application/json':
			request_data = request.form
		else:
			request_data = request.get_json()

		challenge_id = request_data.get('challenge_id')

		if current_user.is_admin():
			preview = request.args.get('preview', False)
			if preview:
				challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()
				chal_class = get_chal_class(challenge.type)
				status, message = chal_class.attempt(challenge, request)

				return {
					'success': True,
					'data': {
						'status': "correct" if status else "incorrect",
						'message': message
					}
				}

		if ctf_paused():
			return {
				'success': True,
				'data': {
					'status': "paused",
					'message': '{} is paused'.format(config.ctf_name())
				}
			}, 403

		user = get_current_user()
		team = get_current_team()

		fails = Fails.query.filter_by(
			account_id=user.account_id,
			challenge_id=challenge_id
		).count()

		challenge = Challenges.query.filter_by(
			id=challenge_id).first_or_404()

		if challenge.state == 'hidden':
			abort(404)

		if challenge.state == 'locked':
			abort(403)

		if challenge.requirements:
			requirements = challenge.requirements.get('prerequisites', [])
			solve_ids = Solves.query \
				.with_entities(Solves.challenge_id) \
				.filter_by(account_id=user.account_id) \
				.order_by(Solves.challenge_id.asc()) \
				.all()
			solve_ids = set([solve_id for solve_id, in solve_ids])
			prereqs = set(requirements)
			if solve_ids >= prereqs:
				pass
			else:
				abort(403)

		chal_class = get_chal_class(challenge.type)

		# Anti-bruteforce / submitting Flags too quickly
		if current_user.get_wrong_submissions_per_minute(session['id']) > 10:
			if ctftime():
				chal_class.fail(
					user=user,
					team=team,
					challenge=challenge,
					request=request
				)
			log(
				'submissions',
				"[{date}] {name} submitted {submission} with kpm {kpm} [TOO FAST]",
				submission=request_data['submission'].encode('utf-8'),
				kpm=current_user.get_wrong_submissions_per_minute(session['id'])
			)
			# Submitting too fast
			return {
				'success': True,
				'data': {
					'status': "ratelimited",
					'message': "You're submitting flags too fast. Slow down."
				}
			}, 429

		solves = Solves.query.filter_by(
			account_id=user.account_id,
			challenge_id=challenge_id
		).first()

		# Challenge not solved yet
		if not solves:
			# Hit max attempts
			max_tries = challenge.max_attempts
			if max_tries and fails >= max_tries > 0:
				return {
					'success': True,
					'data': {
						'status': "incorrect",
						'message': "You have 0 tries remaining"
					}
				}, 403

			status, message = chal_class.attempt(challenge, request)
			if status:  # The challenge plugin says the input is right
				if ctftime() or current_user.is_admin():
					chal_class.solve(
						user=user,
						team=team,
						challenge=challenge,
						request=request
					)
					clear_standings()

				log(
					'submissions',
					"[{date}] {name} submitted {submission} with kpm {kpm} [CORRECT]",
					submission=request_data['submission'].encode('utf-8'),
					kpm=current_user.get_wrong_submissions_per_minute(
						session['id'])
				)
				return {
					'success': True,
					'data': {
						'status': "correct",
						'message': message
					}
				}
			else:  # The challenge plugin says the input is wrong
				if ctftime() or current_user.is_admin():
					chal_class.fail(
						user=user,
						team=team,
						challenge=challenge,
						request=request,
						share=message=="Share Flag Detected"
					)
					clear_standings()

				log(
					'submissions',
					"[{date}] {name} submitted {submission} with kpm {kpm} [WRONG]",
					submission=request_data['submission'].encode('utf-8'),
					kpm=current_user.get_wrong_submissions_per_minute(
						session['id'])
				)

				if max_tries:
					# Off by one since fails has changed since it was gotten
					attempts_left = max_tries - fails - 1
					tries_str = 'tries'
					if attempts_left == 1:
						tries_str = 'try'
					# Add a punctuation mark if there isn't one
					if message[-1] not in '!().;?[]{}':
						message = message + '.'
					return {
						'success': True,
						'data': {
							'status': "incorrect",
							'message': '{} You have {} {} remaining.'.format(message, attempts_left, tries_str)
						}
					}
				else:
					return {
						'success': True,
						'data': {
							'status': "incorrect",
							'message': message
						}
					}

		# Challenge already solved
		else:
			status, message = chal_class.attempt(challenge, request)

			return {
				'success': True,
				'data': {
					'status': "already_solved",
					'message': "You already solved this "+("and the flag is correct" if status else "but the flag is wrong")
				}
			}
			log(
				'submissions',
				"[{date}] {name} submitted {submission} with kpm {kpm} [ALREADY SOLVED]",
				submission=request_data['submission'].encode('utf-8'),
				kpm=current_user.get_wrong_submissions_per_minute(
					user.account_id
				)
			)
			# return {
			#     'success': True,
			#     'data': {
			#         'status': "already_solved",
			#         'message': 'You already solved this'
			#     }
			# }


@challenges_namespace.route('/<challenge_id>/solves')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeSolves(Resource):
	@check_challenge_visibility
	@check_score_visibility
	@during_ctf_time_only
	@require_verified_emails
	def get(self, challenge_id):
		response = []
		challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()

		# TODO: Need a generic challenge visibility call.
		# However, it should be stated that a solve on a gated challenge is not considered private.
		if challenge.state == 'hidden' and is_admin() is False:
			abort(404)

		Model = get_model()

		solves = Solves.query.join(Model, Solves.account_id == Model.id)\
			.filter(Solves.challenge_id == challenge_id, Model.banned == False, Model.hidden == False)\
			.order_by(Solves.date.asc())

		endpoint = None
		if get_config('user_mode') == TEAMS_MODE:
			endpoint = 'teams.public'
			arg = 'team_id'
		elif get_config('user_mode') == USERS_MODE:
			endpoint = 'users.public'
			arg = 'user_id'

		for solve in solves:
			response.append({
				'account_id': solve.account_id,
				'name': solve.account.name,
				'date': isoformat(solve.date),
				'account_url': url_for(endpoint, **{arg: solve.account_id})
			})

		return {
			'success': True,
			'data': response
		}


@challenges_namespace.route('/<challenge_id>/files')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeFiles(Resource):
	@admins_only
	def get(self, challenge_id):
		response = []

		challenge_files = ChallengeFilesModel.query.filter_by(
			challenge_id=challenge_id).all()

		for f in challenge_files:
			response.append({
				'id': f.id,
				'type': f.type,
				'location': f.location
			})
		return {
			'success': True,
			'data': response
		}


@challenges_namespace.route('/<challenge_id>/tags')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeTags(Resource):
	@admins_only
	def get(self, challenge_id):
		response = []

		tags = Tags.query.filter_by(challenge_id=challenge_id).all()

		for t in tags:
			response.append({
				'id': t.id,
				'challenge_id': t.challenge_id,
				'value': t.value
			})
		return {
			'success': True,
			'data': response
		}


@challenges_namespace.route('/<challenge_id>/hints')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeHints(Resource):
	@admins_only
	def get(self, challenge_id):
		hints = Hints.query.filter_by(challenge_id=challenge_id).all()
		schema = HintSchema(many=True)
		response = schema.dump(hints)

		if response.errors:
			return {
				'success': False,
				'errors': response.errors
			}, 400

		return {
			'success': True,
			'data': response.data
		}


@challenges_namespace.route('/<challenge_id>/flags')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeFlags(Resource):
	@admins_only
	def get(self, challenge_id):
		flags = Flags.query.filter_by(challenge_id=challenge_id).all()
		schema = FlagSchema(many=True)
		response = schema.dump(flags)

		if response.errors:
			return {
				'success': False,
				'errors': response.errors
			}, 400

		return {
			'success': True,
			'data': response.data
		}

@challenges_namespace.route('/<challenge_id>/announce')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeAnnounce(Resource):
	@admins_only
	def post(self, challenge_id):
		chal = Challenges.query.filter(Challenges.id == challenge_id).first_or_404()
		from fyp import announceDiscord, selectCategory
		announceDiscord(f"A new challenge has created!\n**{chal.name}** in **{selectCategory(chal.category_id).name}** category")
		return {
				'success': True
		}

@challenges_namespace.route('/<challenge_id>/writeup')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeWriteup(Resource):
	@check_challenge_visibility
	@require_verified_emails
	def get(self, challenge_id):
		response = []

		writeups = Writeups.query.filter_by(challenge_id=challenge_id).all()

		endpoint = 'users.public'
		arg = 'user_id'

		for w in writeups:
			user = Users.query.filter_by(id=w.user_id).first_or_404()
			response.append({
				"link":w.link,
				"author":user.name,
				'account_url': url_for(endpoint, **{arg: user.id})
			})

		return {
			'success': True,
			'data': response
		}

	def post(self, challenge_id):
		if authed() is False:
			return {
				'success': True,
				'data': {
					'status': "authentication_required",
				}
			}, 403

		if request.content_type != 'application/json':
			request_data = request.form
		else:
			request_data = request.get_json()
		user = get_current_user()
		writeup = Writeups(
			user_id=user.id,
			challenge_id = challenge_id,
			link = request_data.get("link")
		)
		db.session.add(writeup)
		db.session.commit()
		return {
			'success': True
		}

@challenges_namespace.route('/<challenge_id>/like')
@challenges_namespace.param('id', 'A Challenge ID')
class ChallengeWriteup(Resource):
	@check_challenge_visibility
	@require_verified_emails
	def post(self, challenge_id):
		if authed() is False:
			return {
				'success': True,
				'data': {
					'status': "authentication_required",
				}
			}, 403

		user = get_current_user()
		like = Likes.checkUserLike(challenge_id)
		if like.count():
			db.session.delete(like.first())
		else:
			like = Likes(
				user_id=user.id,
				challenge_id = challenge_id
			)
			db.session.add(like)
		db.session.commit()
		return {
			'success': True
		}
