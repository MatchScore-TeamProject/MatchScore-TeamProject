
# Email Body for Link Requests

def approved_scenario_lr(name_of_receiver: str):
    body = f"""Dear {name_of_receiver},
    
     We are pleased to inform you that your request to link your profile has been successfully approved. This linkage will enable you to access enhanced features, connect with more peers, and engage more deeply with our network.
    
     If you have any questions or require further assistance, please do not hesitate to contact our support team at matchscorecustomersupport@gmail.com.
    
     Thank you for being a valued member of our community. We look forward to seeing the great connections and contributions you will make.
    
     Best regards,
    
    D.G.R
    CEO
    MatchScoreCompany"""

    return body


def denied_scenario_lr(name_of_receiver: str):
    body = f"""
    Dear {name_of_receiver},
    
     Thank you for submitting your request to link your profile. After careful review, we regret to inform you that we are unable to approve your request at this time.
    
     This decision was based on eligibility criteria not met. We encourage you to review our guidelines and ensure that all necessary criteria are met before re-submitting your request.
    
     We understand that this may be disappointing, and we are here to assist you in meeting the requirements for a successful profile linkage. For further guidance or to discuss this matter, please feel free to contact our support team at matchscorecustomersupport@gmail.com.
    
     We appreciate your understanding and look forward to assisting you in successfully linking your profile in the future.
    
    Sincerely,
    
    D.G.R
    CEO
    MatchScoreCompany
"""

    return body


# Email Body for Promote Requests
def approved_scenario_pr(name_of_receiver: str):
    body = f"""Dear {name_of_receiver},

     We are thrilled to inform you that your request for promotion to the position of Director has been approved. Your dedication, hard work, and contributions to our team have been exceptional, and we believe you are well-deserving of this advancement.
    
     As a Director, you will play a pivotal role in shaping the future of our department and organization. We are confident in your abilities to lead with excellence and inspire those around you.
    
     After a few days we will need to discuss the next steps and your new responsibilities. We are excited to see you grow in this new role and contribute even more to our collective success.
    
     Congratulations once again on this well-deserved promotion!
    
    Warm regards,
    
    D.G.R
    CEO
    MatchScoreCompany
"""
    return body


def denied_scenario_pr(name_of_receiver: str):
    body = f"""Dear {name_of_receiver},

     Thank you for your interest in the Director position and for your ongoing contributions to our team. After careful consideration, we regret to inform you that we are unable to approve your promotion request at this time.
    
     This decision does not diminish the value of your work and dedication to our organization. We recognize your potential and encourage you to continue your professional development.
    
     We are committed to your professional growth and would like to offer you the opportunity to work with a mentor or engage in specific training programs to prepare for future leadership opportunities.
    
     Please feel free to schedule a meeting with me to discuss your career path and how we can support your aspirations within our organization.
    
    Thank you again for your hard work and commitment.
    
    Sincerely,

    D.G.R
    CEO
    MatchScoreCompany
"""

    return body


def add_to_match_scenario(participants: list, date: str):

    body = f"""Dear Participant,

     Great news! You have been added to an upcoming match.
    
     Match Details:
        - Participants: {participants[0]}, {participants[1]}
        - Date: {date}
        
     It's important to be prepared and on time for the match to ensure a fair and enjoyable experience for everyone involved.
    
     For any queries or further details, feel free to reach out to us.
    
     Wishing you the best of luck in your upcoming match!
    
    Best regards,

    D.G.R
    CEO
    MatchScoreCompany
"""

    return body


def add_to_tournament_scenario(participants: list[str], date: str, tournament_format: str, tournament_name: str):

    body = f"""Dear Participant,

     We are excited to announce that you have been successfully added to the {tournament_name}! This tournament promises to be a thrilling event, and we are delighted to have you as part of it.
    
     Tournament Details:
        - Date: {date}
        - Tournament Format: {tournament_format}
        - Participants: {", ".join([participant for participant in participants])}
    
     It is important to familiarize yourself with these to ensure a smooth and enjoyable experience.
    
     Should you have any questions or require further information, please do not hesitate to contact us.
    
     Best of luck, and we look forward to seeing your performance!

    Warm regards,

    D.G.R
    CEO
    MatchScoreCompany
"""
    return body


def changed_match_date_scenario(new_date: str):
    body = f"""Dear Participant,

     We would like to inform you of a change in the details of your upcoming match.
    
     Updated Match Details: 
        - New Date: {new_date}

     We apologize for any inconvenience this change may cause and appreciate your understanding and flexibility. These changes are made to ensure the best possible experience for all participants.
    
     For any concerns or further assistance, do not hesitate to contact us.
    
     Thank you for your cooperation, and we wish you the best in your upcoming match!
    
    Warm regards,

    D.G.R
    CEO
    MatchScoreCompany
"""

    return body
