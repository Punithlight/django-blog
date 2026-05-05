from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from blogs.models import Blog, Category


class Command(BaseCommand):
    help = 'Creates Manager, Editor, Author groups and sample users'

    def handle(self, *args, **kwargs):

        # ── Content types ──────────────────────────────────────────
        blog_ct     = ContentType.objects.get_for_model(Blog)
        category_ct = ContentType.objects.get_for_model(Category)
        user_ct     = ContentType.objects.get_for_model(User)

        # ── Permissions ────────────────────────────────────────────
        blog_perms     = Permission.objects.filter(content_type=blog_ct)
        category_perms = Permission.objects.filter(content_type=category_ct)
        user_perms     = Permission.objects.filter(content_type=user_ct)

        editor_blog_perms = Permission.objects.filter(
            content_type=blog_ct,
            codename__in=['add_blog', 'delete_blog', 'view_blog']
        )

        # ── MANAGER group (all permissions) ────────────────────────
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        manager_group.permissions.set(
            list(blog_perms) + list(category_perms) + list(user_perms)
        )
        self.stdout.write(self.style.SUCCESS('Manager group created/updated'))

        # ── EDITOR group (add, delete, view blog only) ─────────────
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        editor_group.permissions.set(list(editor_blog_perms))
        self.stdout.write(self.style.SUCCESS('Editor group created/updated'))

        # ── AUTHOR group (can comment — no special permissions) ────
        author_group, _ = Group.objects.get_or_create(name='Author')
        author_group.permissions.clear()
        self.stdout.write(self.style.SUCCESS('Author group created/updated'))

        # ── CREATE USERS ───────────────────────────────────────────

        # Manager user
        if not User.objects.filter(username='manager').exists():
            manager_user = User.objects.create_user(
                username='manager',
                password='mana1234',
                email='manager@blog.com',
                is_staff=True,
            )
            manager_user.groups.add(manager_group)
            self.stdout.write(self.style.SUCCESS('User "manager" created'))
        else:
            self.stdout.write(self.style.WARNING('User "manager" already exists, skipped'))

        # Editor user
        if not User.objects.filter(username='editor').exists():
            editor_user = User.objects.create_user(
                username='editor',
                password='edit1234',
                email='editor@blog.com',
                is_staff=True,
            )
            editor_user.groups.add(editor_group)
            self.stdout.write(self.style.SUCCESS('User "editor" created'))
        else:
            self.stdout.write(self.style.WARNING('User "editor" already exists, skipped'))

        # Author user
        if not User.objects.filter(username='author').exists():
            author_user = User.objects.create_user(
                username='author',
                password='auth1234',
                email='author@blog.com',
                is_staff=False,
            )
            author_user.groups.add(author_group)
            self.stdout.write(self.style.SUCCESS('User "author" created'))
        else:
            self.stdout.write(self.style.WARNING('User "author" already exists, skipped'))

        self.stdout.write(self.style.SUCCESS('\nAll done! Roles and users are ready.'))
