import smtplib
import ssl
from email.message import EmailMessage

import db_password
from models.options import CurrentStatus, EmailType
from services.email_bodies import approved_scenario_lr, denied_scenario_lr, approved_scenario_pr, \
    denied_scenario_pr, add_to_match_scenario, add_to_tournament_scenario, changed_match_date_scenario

email_sender = "matchscorea51@gmail.com"
email_password = db_password.em_password


def send_email_for_requests(receiver: str, conformation: str, email_type: str):
    email_receiver = receiver
    subject = ""
    body = ""

    name_of_receiver = receiver.split("@")[0]

    if conformation == CurrentStatus.APPROVED.value and email_type == EmailType.LINK_REQUEST.value:
        subject = "Your Link-Profile Request Has Been Successfully Approved"
        body = approved_scenario_lr(name_of_receiver)

    if conformation == CurrentStatus.DENIED.value and email_type == EmailType.LINK_REQUEST.value:
        subject = "Update on Your Link-Request"
        body = denied_scenario_lr(name_of_receiver)

    if conformation == CurrentStatus.APPROVED.value and email_type == EmailType.PROMOTE_REQUEST.value:
        subject = "Congratulations! Your Promotion to Director Has Been Approved"
        body = approved_scenario_pr(name_of_receiver)
    if conformation == CurrentStatus.DENIED.value and email_type == EmailType.PROMOTE_REQUEST.value:
        subject = "Regarding Your Promotion to Director Request"
        body = denied_scenario_pr(name_of_receiver)

    if receiver is not None:
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_email_for_added_to_event(receiver: str, participants: list, date: str, email_type: str,
                                  format_tournament: str = None,
                                  tournament_name: str = None):
    email_receiver = receiver
    subject = ""
    body = ""

    if email_type == EmailType.ADDED_TO_MATCH.value:
        subject = "You've Been Added to a Match!"
        body = add_to_match_scenario(participants, date)

    if email_type == EmailType.ADDED_TO_TOURNAMENT.value:
        subject = f"Welcome to the {tournament_name}!"
        body = add_to_tournament_scenario(participants, date, format_tournament, tournament_name)

    if receiver is not None:
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_email_changed_match_date(receiver: str, new_date: str, email_type: str):
    email_receiver = receiver
    subject = ""
    body = ""

    if email_type == EmailType.MATCH_CHANGED.value:
        subject = "Notice of Change in Match Details"
        body = changed_match_date_scenario(new_date)

    if receiver is not None:
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
