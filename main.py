from datetime import datetime

from constants import DATETIME_FORMAT
from cowin_client import CoWinClient
from twilio_client import TwilioClient
from utilities import get_active_users, get_active_district_ids, update_last_notified


def send_alerts():
    district_ids = get_active_district_ids()
    for district_id in district_ids:
        print('Sending alerts for district_id: {}'.format(district_id))
        send_district_alerts(district_id)


def send_district_alerts(district_id: int):
    capacity_dict = get_capacity(district_id)
    print(f'Under 45 capacity: {capacity_dict}')

    # message to be sent via WhatsApp
    message = (f'COVID-19 vaccine slots are available for the age group 18 to 44.\n'
               f'Availability:\nDose 1: {capacity_dict["dose_1"]}\nDose 2: {capacity_dict["dose_2"]}'
               f'\nPlease book your slot at {CoWinClient.registration_url}')

    # if capacity more than 5 then find the active users and notify them via WhatsApp
    if capacity_dict['total'] >= 5:
        users = get_active_users(district_id=district_id)
        recipient_phone_numbers = []
        now = datetime.now()
        print(f'users before filtering: {users}')
        for user in users:  # only the users who have not been notified in past 3 hours have to be notified
            last_notified = user['last_notified'] and datetime.strptime(user['last_notified'], DATETIME_FORMAT)
            if last_notified:
                time_diff = now - last_notified
                num_seconds_in_3_hours = 3 * 60 * 60
                if time_diff.total_seconds() > num_seconds_in_3_hours:
                    recipient_phone_numbers.append((user['id'], user['phone']))
            else:
                recipient_phone_numbers.append((user['id'], user['phone']))

        # send update via WhatsApp using Twilio API
        client = TwilioClient()
        for user_id, to_number in recipient_phone_numbers:
            res = client.send_whats_app_message(to_number, message)
            if res:  # update last_notified after successfully sending notification via WhatsApp
                update_last_notified(user_id)


def get_capacity(district_id):
    client = CoWinClient(district_id)
    capacity = client.get_under_45_capacity()
    # capacity = client.get_capacity_for_minimum_age(20)
    return capacity


if __name__ == '__main__':
    send_alerts()
