# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailHost'
        db.create_table('mail_mailhost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('host_port', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('host_ssl', self.gf('django.db.models.fields.BooleanField')()),
            ('host_authentication', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('mail', ['MailHost'])

        # Adding model 'MailAccount'
        db.create_table('mail_mailaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender_name', self.gf('django.db.models.fields.CharField')(null=True, max_length=60, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=60)),
            ('logon_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('mail_account_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('retrieve_host', self.gf('django.db.models.fields.related.OneToOneField')(related_name='retrieve_host_of', unique=True, to=orm['mail.MailHost'])),
            ('send_host', self.gf('django.db.models.fields.related.OneToOneField')(related_name='send_host_of', unique=True, to=orm['mail.MailHost'])),
        ))
        db.send_create_signal('mail', ['MailAccount'])

        # Adding model 'MailBox'
        db.create_table('mail_mailbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('mail_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mail.MailAccount'])),
        ))
        db.send_create_signal('mail', ['MailBox'])

        # Adding model 'Message'
        db.create_table('mail_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mail_box', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mail.MailBox'])),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('subject', self.gf('django.db.models.fields.CharField')(null=True, max_length=180, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('mail_source', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mail', ['Message'])

        # Adding model 'Recipient'
        db.create_table('mail_recipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adress', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(null=True, max_length=60, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipients', to=orm['mail.Message'])),
        ))
        db.send_create_signal('mail', ['Recipient'])


    def backwards(self, orm):
        # Deleting model 'MailHost'
        db.delete_table('mail_mailhost')

        # Deleting model 'MailAccount'
        db.delete_table('mail_mailaccount')

        # Deleting model 'MailBox'
        db.delete_table('mail_mailbox')

        # Deleting model 'Message'
        db.delete_table('mail_message')

        # Deleting model 'Recipient'
        db.delete_table('mail_recipient')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mail.mailaccount': {
            'Meta': {'object_name': 'MailAccount'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logon_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'mail_account_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'retrieve_host': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'retrieve_host_of'", 'unique': 'True', 'to': "orm['mail.MailHost']"}),
            'send_host': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'send_host_of'", 'unique': 'True', 'to': "orm['mail.MailHost']"}),
            'sender_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '60', 'blank': 'True'})
        },
        'mail.mailbox': {
            'Meta': {'object_name': 'MailBox'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.MailAccount']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'mail.mailhost': {
            'Meta': {'object_name': 'MailHost'},
            'host_authentication': ('django.db.models.fields.BooleanField', [], {}),
            'host_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'host_port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'host_ssl': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mail.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'mail_box': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.MailBox']"}),
            'mail_source': ('django.db.models.fields.TextField', [], {}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'subject': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '180', 'blank': 'True'})
        },
        'mail.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'adress': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipients'", 'to': "orm['mail.Message']"}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '60', 'blank': 'True'})
        }
    }

    complete_apps = ['mail']