import keyboards as kbds

############
# FEEDBACK #
############

fb_title_msg = 'Please state the issue subject.'
fb_details_msg = 'Please provide more details about this issue. \
You can also leave a simple "-" or "NA"'
fb_file_msg = 'Do you want to upload a file for this issue?\n\
/no if you do not want to submit a file.'
fb_complete_msg = 'Thank you for your feedback. A Moderator will respond to \
you ASAP'
fb_sumview_temp = '**{id}**: __{title}__'
fb_detview_temp = """__{id}: {title}__ 
{msg}"""

## REPORTING
report_cat = '''You are making a report on the partner of your your last conversation
What is the reason for this report?
'''
report_title = "Please summarise your report to create a title"
report_msg = 'Please describe the problem with as much detail as possible'
report_complete = '''Thank you for completing this report, our admins will work on it asap!
A message will be sent to you when this matter is resolved. Please do not duplicate reports as it only \
slows down the process.
'''

## Pairing
pair_found = {
    "text": 'Pair found! Say hello to your partner. These are the following functions you may need:\n1. /unpair to end conversation.\n2. /share_telehandle to share your telegram handle.\n3. /request_telehandle to request for your partner to share his/her telegram handle.',
    "reply_markup": kbds.pair_found
}