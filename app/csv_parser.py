from flask import current_app
import csv
import io
import re

phone_number_regex = re.compile('^\\+44[\\d]{10}$')


def transform_sms(csv_file):
    return transform(csv_file, 'sms')


def transform(csv_file, type):
    notifications = []
    errors = []
    csv_reader = csv.reader(csv_file)
    for idx, row in enumerate(csv_reader):
        if idx + 1 > current_app.config['MAX_ROWS_IN_BULK_UPLOAD']:
            return {
                'errors': [{
                    'error': 'MAX number of rows ({}) exceeded'.format(current_app.config['MAX_ROWS_IN_BULK_UPLOAD'])
                }]
            }
        if len(row) == 3 and validate_sms_message(row[1], row[2]):
            notifications.append({
                'to': row[1],
                'message': row[2]
            })
        else:
            errors.append("Row ({}) is invalid".format(idx + 1))
    if len(errors) > 0:
        return {
            'errors': errors
        }

    return {
        'notifications': notifications
    }


def validate_sms_message(to, message):
    if phone_number_regex.match(to) and len(message) < current_app.config['MAX_MESSAGE_LENGTH_FOR_SMS']:
        return True
    else:
        return False


def validate_email_message():
    return True


def validate_phone_number():
    return True


def validate_email_address():
    return True
