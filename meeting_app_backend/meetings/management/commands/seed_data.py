from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from meetings.models import Meeting, Subject, Owner, Comment
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create users (in addition to superuser 'admin')
        user1, created = User.objects.get_or_create(
            username='user1',
            defaults={'password': 'user123', 'email': 'user1@example.com'}
        )
        if created:
            user1.set_password('user123')  # Hash the password
            user1.save()
            self.stdout.write(self.style.SUCCESS('Created user: user1'))

        user2, created = User.objects.get_or_create(
            username='user2',
            defaults={'password': 'user123', 'email': 'user2@example.com'}
        )
        if created:
            user2.set_password('user123')  # Hash the password
            user2.save()
            self.stdout.write(self.style.SUCCESS('Created user: user2'))

        # Get the admin user (assumes superuser 'admin' exists from Step 1)
        try:
            admin = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found. Please create a superuser with username "admin".'))
            return

        # Create meetings
        meeting1, _ = Meeting.objects.get_or_create(
            title='Team Sync',
            defaults={
                'description': 'Weekly team synchronization meeting',
                'created_by': admin
            }
        )
        self.stdout.write(self.style.SUCCESS('Created meeting: Team Sync'))

        meeting2, _ = Meeting.objects.get_or_create(
            title='Project Kickoff',
            defaults={
                'description': 'Kickoff meeting for new project',
                'created_by': user1
            }
        )
        self.stdout.write(self.style.SUCCESS('Created meeting: Project Kickoff'))

        # Create subjects
        subject1, _ = Subject.objects.get_or_create(
            meeting=meeting1,
            title='Budget Review',
            defaults={
                'description': 'Discuss Q2 budget allocations',
                'status': Subject.STATUS_ACTIVE
            }
        )
        self.stdout.write(self.style.SUCCESS('Created subject: Budget Review'))

        subject2, _ = Subject.objects.get_or_create(
            meeting=meeting1,
            title='Project Update',
            defaults={
                'description': 'Update on project milestones',
                'status': Subject.STATUS_ON_HOLD,
                'on_hold_until': date.today() + timedelta(days=7)  # 7 days from today
            }
        )
        self.stdout.write(self.style.SUCCESS('Created subject: Project Update'))

        subject3, _ = Subject.objects.get_or_create(
            meeting=meeting2,
            title='Resource Planning',
            defaults={
                'description': 'Plan resource allocation for project',
                'status': Subject.STATUS_CLOSED
            }
        )
        self.stdout.write(self.style.SUCCESS('Created subject: Resource Planning'))

        subject4, _ = Subject.objects.get_or_create(
            meeting=meeting2,
            title='Risk Assessment',
            defaults={
                'description': 'Identify potential project risks',
                'status': Subject.STATUS_ACTIVE
            }
        )
        self.stdout.write(self.style.SUCCESS('Created subject: Risk Assessment'))

        # Assign owners
        Owner.objects.get_or_create(user=user1, subject=subject1)
        Owner.objects.get_or_create(user=user2, subject=subject1)
        Owner.objects.get_or_create(user=admin, subject=subject2)
        Owner.objects.get_or_create(user=user1, subject=subject3)
        Owner.objects.get_or_create(user=user2, subject=subject4)
        self.stdout.write(self.style.SUCCESS('Assigned owners to subjects'))

        # Create comments
        Comment.objects.get_or_create(
            meeting=meeting1,
            user=admin,
            text='Please prepare budget reports.',
            defaults={'created_at': date.today()}
        )
        Comment.objects.get_or_create(
            meeting=meeting1,
            subject=subject1,
            user=user1,
            text='Q2 budget looks tight.',
            defaults={'created_at': date.today()}
        )
        Comment.objects.get_or_create(
            meeting=meeting2,
            user=user2,
            text='Excited for the project kickoff!',
            defaults={'created_at': date.today()}
        )
        Comment.objects.get_or_create(
            meeting=meeting2,
            subject=subject4,
            user=admin,
            text='Need to discuss risk mitigation strategies.',
            defaults={'created_at': date.today()}
        )
        self.stdout.write(self.style.SUCCESS('Created comments'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))