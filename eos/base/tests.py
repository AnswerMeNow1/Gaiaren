#   Eos - Verifiable elections
#   Copyright © 2017  RunasSudo (Yingtong Li)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from eos.base.election import *
from eos.base.workflow import *
from eos.core.objects import *

class ElectionTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		client.drop_database('test')
	
	def test_run_election(self):
		# Set up election
		election = Election()
		election.workflow = WorkflowBase(election)
		
		self.assertEqual(election.workflow.get_task('eos.base.workflow.TaskConfigureElection').status, WorkflowTask.Status.READY)
		
		election.name = 'Test Election'
		
		for i in range(3):
			election.voters.append(Voter())
		
		question = ApprovalQuestion()
		question.prompt = 'President'
		question.choices.append('John Smith')
		question.choices.append('Joe Bloggs')
		question.choices.append('John Q. Public')
		election.questions.append(question)
		
		question = ApprovalQuestion()
		question.prompt = 'Chairman'
		question.choices.append('John Doe')
		question.choices.append('Andrew Citizen')
		election.questions.append(question)
		
		#election.save()
		
		# Check that it saved
		#self.assertEqual(Election.objects.get(0)._id, election._id) # TODO: Compare JSON
		
		# Retrieve from scratch, too
		#self.db.close()
		#self.db = mongoengine.connect('test')
		#self.assertEqual(Election.objects.get(0)._id, election._id)
		
		# Freeze election
		self.assertEqual(election.workflow.get_task('eos.base.workflow.TaskConfigureElection').status, WorkflowTask.Status.READY)
		self.assertEqual(election.workflow.get_task('eos.base.workflow.TaskOpenVoting').status, WorkflowTask.Status.NOT_READY)
		election.workflow.get_task('eos.base.workflow.TaskConfigureElection').exit()
		self.assertEqual(election.workflow.get_task('eos.base.workflow.TaskConfigureElection').status, WorkflowTask.Status.EXITED)
		self.assertEqual(election.workflow.get_task('eos.base.workflow.TaskOpenVoting').status, WorkflowTask.Status.READY)