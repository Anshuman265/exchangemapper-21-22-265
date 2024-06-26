# Generated by Django 3.2.6 on 2021-10-05 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('upvote', models.IntegerField(default=0)),
                ('downvote', models.IntegerField(default=0)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('fullname', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ('fullname',),
            },
        ),
        migrations.CreateModel(
            name='HomeCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=400, null=True)),
                ('season', models.CharField(choices=[('S', 'Spring'), ('A', 'Autumn')], default='S', max_length=1)),
                ('year', models.CharField(choices=[('2', 'Second year'), ('3', 'Third year'), ('4', 'Fourth year'), ('5', 'Dual Degree')], default='2', max_length=1)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.department')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=500)),
                ('country', models.CharField(default=0, max_length=60)),
            ],
            options={
                'ordering': ('fullname',),
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('roll_number', models.CharField(max_length=20)),
                ('department', models.CharField(blank=True, max_length=200, null=True)),
                ('join_year', models.IntegerField(blank=True, null=True)),
                ('graduation_year', models.IntegerField(blank=True, null=True)),
                ('degree', models.CharField(blank=True, max_length=300, null=True)),
                ('email_ldap', models.CharField(max_length=200)),
                ('downvoted', models.ManyToManyField(related_name='downuser', to='main.Answer')),
                ('upvoted', models.ManyToManyField(related_name='upuser', to='main.Answer')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userinfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=400, null=True)),
                ('department', models.CharField(max_length=400, null=True)),
                ('season', models.CharField(choices=[('S', 'Spring'), ('A', 'Autumn')], default='S', max_length=1)),
                ('year', models.CharField(choices=[('2', 'Second year'), ('3', 'Third year'), ('4', 'Fourth year'), ('5', 'Dual Degree')], default='2', max_length=1)),
                ('UserInfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userinfo')),
                ('homecourse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.homecourse')),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.university')),
            ],
        ),
        migrations.CreateModel(
            name='Expierence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('para1', models.CharField(max_length=400, null=True)),
                ('para2', models.CharField(max_length=400, null=True)),
                ('para3', models.CharField(max_length=400, null=True)),
                ('img1', models.ImageField(upload_to='images/')),
                ('img2', models.ImageField(upload_to='images/')),
                ('img3', models.ImageField(upload_to='images/')),
                ('iframe', models.CharField(max_length=400, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('UserInfo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userinfo')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
        migrations.CreateModel(
            name='Doubt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userinfo')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
        migrations.CreateModel(
            name='CourseMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('University', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.university')),
                ('UserInfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userinfo')),
                ('remote_courses', models.ManyToManyField(to='main.RemoteCourse')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.expierence')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userinfo')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userinfo'),
        ),
        migrations.AddField(
            model_name='answer',
            name='doubt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.doubt'),
        ),
    ]
