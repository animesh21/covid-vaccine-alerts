from datetime import datetime

import requests


class CoWinClient(object):
    home_url = 'https://www.cowin.gov.in/'
    registration_url = 'https://selfregistration.cowin.gov.in/'
    date_str = datetime.now().strftime('%d-%m-%Y')

    def __init__(self, district_id):
        self.district_id = district_id
        self.url = (f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?'
                    f'district_id={self.district_id}&date={self.date_str}')

    def get_under_45_capacity(self):
        """
        Fetches data from CoWin portal for self.district_id and returns a dict with dose 1, dose 2 and
        total availability
        :return: dict, e.g. { 'total': 100, 'dose_1': 55, 'dose_2': 45 }
        """
        headers = self.get_request_headers()
        res = requests.get(self.url, headers=headers)
        res_json = res.json()
        all_centers = res_json.get('centers') or []
        under_45_name_suffix = '18 to 44'
        under_45_centers = [center for center in all_centers
                            if under_45_name_suffix in center['name'].lower()]
        print(f'Total under 45 centers: {len(under_45_centers)}')
        total_capacity = {
            'total': 0,
            'dose_1': 0,
            'dose_2': 0,
        }
        for center in under_45_centers:
            center_capacity = {
                'total': 0,
                'dose_1': 0,
                'dose_2': 0,
            }
            for session in center['sessions']:
                center_capacity['total'] += session['available_capacity']
                center_capacity['dose_1'] += session['available_capacity_dose1']
                center_capacity['dose_2'] += session['available_capacity_dose2']
            total_capacity['total'] += center_capacity['total']
            total_capacity['dose_1'] += center_capacity['dose_1']
            total_capacity['dose_2'] += center_capacity['dose_2']
            print(f"{center['name']}: {center_capacity}")
        return total_capacity

    def get_capacity_for_minimum_age(self, min_age):
        headers = self.get_request_headers()
        res = requests.get(self.url, headers=headers)
        res_json = res.json()
        all_centers = res_json.get('centers') or []
        print(f'Total centers: {len(all_centers)}')
        total_capacity = {
            'total': 0,
            'dose_1': 0,
            'dose_2': 0,
        }
        total_number_of_centers = 0
        for center in all_centers:
            center_capacity = {
                'total': 0,
                'dose_1': 0,
                'dose_2': 0,
            }
            for session in center['sessions']:
                if session['min_age_limit'] <= min_age:
                    center_capacity['total'] += session['available_capacity']
                    center_capacity['dose_1'] += session['available_capacity_dose1']
                    center_capacity['dose_2'] += session['available_capacity_dose2']
            if center_capacity['total']:
                total_number_of_centers += 1
                print(f'Center name: {center["name"]}; Capacity: {center_capacity}')
                total_capacity['total'] += center_capacity['total']
                total_capacity['dose_1'] += center_capacity['dose_1']
                total_capacity['dose_2'] += center_capacity['dose_2']
        print(f'# of centers with min age {min_age}: {total_number_of_centers}')
        return total_capacity

    @staticmethod
    def get_request_headers():
        headers = {
            'authority': 'cdn-api.co-vin.in',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/90.0.4430.93 Safari/537.36'),
            'origin': 'https://www.cowin.gov.in',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.cowin.gov.in/',
            'accept-language': 'en_US,en;q=0.9',
            'if-none-match': 'W/"15514-BSMeW8/8h2KpNSRQYKyYKhG3wEg"',
        }
        return headers


if __name__ == '__main__':
    lucknow_district_id = 670
    co_win_client = CoWinClient(lucknow_district_id)
    capacity = co_win_client.get_under_45_capacity()
    # capacity = co_win_client.get_capacity_for_minimum_age(20)
    print(f'Total under 45 capacity: {capacity}')
