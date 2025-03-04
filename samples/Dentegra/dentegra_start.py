import json
from time import sleep
import requests
def run(bot):
    configP = bot.configP
    url = "https://apps.dentegra.com/ciam/login"

    password = ""

    username = ""

    bookmark_titles = ""

    bookmark_values = ""

    base_path = ""

    url_form = ""

    indexes = ""

    index = ""

    is_not_found = ""

    state_verification = ""

    status = ""

    current_row = ""

    policyh_name = ""

    policyh_last_name = ""

    member_id = ""

    policyh_dob = ""

    patient_name = ""

    patient_last_name = ""

    patient_dob = ""

    full_patient_name = ""

    verification_type = ""

    is_login = True

    savepath_form = ""

    relationship = ""

    carrier_name = ""

    state_parameter = ""

    bot_name = "Dentegra"

    clinic_name = ""

    groupid = ""

    term_date = ""

    clinic = ""

    clinics = ""

    primary = ""

    zip_code = ""

    returned_values = ""

    all_indexes = ""

    is_content_loaded = ""

    is_bad_credentials = ""

    verification_start_time = ""

    base_path = 'bot.getvar("base_pathP")'+'Carriers/'+'{bot_name}' + '/'

    clinics = ""
    clinic = ""
    indexes = ""
    index = ""
    all_indexes = ""

    bot.execute_command(module="DentalRobot", command="getIndexes")

