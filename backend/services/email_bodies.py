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
    MatchScoreCompany"""

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
    
     This decision does not diminish the value of your work and dedication to our organization. We recognize your potential and encourage you to continue your professional development. There are specific areas, such as [mention any relevant areas for improvement], where further growth could enhance your readiness for a leadership role in the future.
    
     We are committed to your professional growth and would like to offer you the opportunity to work with a mentor or engage in specific training programs to prepare for future leadership opportunities.
    
     Please feel free to schedule a meeting with me to discuss your career path and how we can support your aspirations within our organization.
    
    Thank you again for your hard work and commitment.
    
    Sincerely,

    D.G.R
    CEO
    MatchScoreCompany
"""

    return body

