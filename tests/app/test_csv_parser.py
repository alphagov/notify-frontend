from io import StringIO
from app.csv_parser import transform_sms, transform_email


def test_should_parse_valid_sms_csv(notify_frontend):
    valid_sms_file = StringIO(open('tests/csv_test_files/valid_sms.csv').read())

    transformed = transform_sms(valid_sms_file)
    assert len(transformed['notifications']) == 4
    assert transformed['notifications'][0]['to'] == '+441212121121'
    assert transformed['notifications'][1]['to'] == '+441212121122'
    assert transformed['notifications'][2]['to'] == '+441212121123'
    assert transformed['notifications'][3]['to'] == '+441212121124'

    assert transformed['notifications'][0]['message'] == 'SMS Message 1'
    assert transformed['notifications'][1]['message'] == 'SMS Message 2'
    assert transformed['notifications'][2]['message'] == 'SMS Message 3'
    assert transformed['notifications'][3]['message'] == 'SMS Message 4'


def test_should_reject_csv_with_too_many_lines(notify_frontend):
    valid_sms_file = StringIO(open('tests/csv_test_files/valid_sms.csv').read())

    notify_frontend.config['MAX_ROWS_IN_BULK_UPLOAD'] = 3
    transformed = transform_sms(valid_sms_file)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0]['error'] == "MAX number of rows (3) exceeded"


def test_should_reject_csv_with_a_bad_phone_number(notify_frontend, notify_config):
    invalid_sms_bad_phone_number = StringIO(open('tests/csv_test_files/invalid_sms_bad_phone_number.csv').read())

    transformed = transform_sms(invalid_sms_bad_phone_number)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0] == "Row (4) is invalid"


def test_should_reject_csv_with_a_bad_message(notify_frontend, notify_config):
    invalid_sms_bad_message = StringIO(open('tests/csv_test_files/invalid_sms_bad_message.csv').read())

    transformed = transform_sms(invalid_sms_bad_message)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0] == "Row (4) is invalid"


def test_should_reject_csv_with_a_bad_message(notify_frontend, notify_config):
    invalid_sms_incorrect_num_columns = StringIO(
        open('tests/csv_test_files/invalid_sms_incorrect_num_columns.csv').read()
    )

    transformed = transform_sms(invalid_sms_incorrect_num_columns)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0] == "Row (3) is invalid"


def test_should_parse_valid_email_csv(notify_frontend):
    valid_email_file = StringIO(open('tests/csv_test_files/valid_email.csv').read())

    transformed = transform_email(valid_email_file)
    assert len(transformed['notifications']) == 2
    assert transformed['notifications'][0]['to'] == 'jo@example.com'
    assert transformed['notifications'][1]['to'] == 'sue@example.com'
    assert transformed['notifications'][0]['from'] == 'example@service.gov.uk'
    assert transformed['notifications'][1]['from'] == 'example@service.gov.uk'
    assert transformed['notifications'][0]['subject'] == 'email test subject'
    assert transformed['notifications'][1]['subject'] == 'email test subject2'
    assert transformed['notifications'][0]['message'] == 'email test message'
    assert transformed['notifications'][1]['message'] == 'email test message2'
    assert transformed['notifications'][0]['description'] == 'email test description'
    assert transformed['notifications'][1]['description'] == 'email test description2'


def test_should_reject_email_with_too_many_lines(notify_frontend):
    valid_file = StringIO(open('tests/csv_test_files/valid_email.csv').read())

    notify_frontend.config['MAX_ROWS_IN_BULK_UPLOAD'] = 1
    transformed = transform_email(valid_file)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0]['error'] == "Max number of rows (1) exceeded"


def test_should_reject_email_with_bad_email_format(notify_frontend):
    notify_frontend.config['MAX_ROWS_IN_BULK_UPLOAD'] = 5
    bad_file = StringIO(open('tests/csv_test_files/bad_email_to_address.csv').read())
    transformed = transform_email(bad_file)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0] == 'Row (1) is invalid'


def test_should_reject_email_with_from_email_a_non_gov_uk_address(notify_frontend):
    bad_file = StringIO(open('tests/csv_test_files/bad_email_from_address.csv').read())
    transformed = transform_email(bad_file)
    assert len(transformed['errors']) == 1
    assert transformed['errors'][0] == 'Row (2) is invalid'
