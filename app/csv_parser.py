from flask import current_app
import csv
import re

phone_number_regex = re.compile('^\\+44[\\d]{10}$')
email_regex = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')
gov_uk_email_regex = re.compile('^[^@^\\s]+@[^@^\\.^\\s]+(\\.[^@^\\.^\\s]*)*.gov.uk')


def transform_sms(csv_file):
    return transform(csv_file, 'sms')


def transform_email(csv_file):
    return transform(csv_file, 'email')


def transform(csv_file, type):
    notifications = []
    errors = []
    csv_reader = csv.reader(csv_file)
    if type == 'sms':
        for idx, row in enumerate(csv_reader):
            if idx + 1 > current_app.config['MAX_ROWS_IN_BULK_UPLOAD']:
                return {
                    'errors': [{
                        'error':
                            'MAX number of rows ({}) exceeded'.format(current_app.config['MAX_ROWS_IN_BULK_UPLOAD'])
                    }]
                }
            if len(row) == 3 and validate_sms_message(row[1], row[2]):
                notifications.append({
                    'to': row[1],
                    'message': row[2]
                })
            else:
                errors.append("Row ({}) is invalid".format(idx + 1))
    if type == 'email':
        for idx, row in enumerate(csv_reader):
            if idx + 1 > current_app.config['MAX_ROWS_IN_BULK_UPLOAD']:
                return {
                    'errors': [{
                        'error':
                            "Max number of rows ({}) exceeded".format(current_app.config['MAX_ROWS_IN_BULK_UPLOAD'])
                    }]
                }
            if len(row) == 7 and validate_email_address(row[1]) and validate_gov_uk_address(row[2]):
                notifications.append({
                    'to': row[1],
                    'from': row[2],
                    'subject': row[3],
                    'message': row[4],
                    'description': row[6]
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


def validate_email_address(email_address):
    if email_regex.match(email_address):
        return True
    else:
        return False


def validate_gov_uk_address(email_address):
    if gov_uk_email_regex.match(email_address):
        return True
    else:
        return False


def validate_phone_number():
    return True
