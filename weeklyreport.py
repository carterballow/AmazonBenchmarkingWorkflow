import pandas as pd
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATA1_FILE_PATH = r'C:\Users\cballow\Documents\GitHub\AmazonBenchmarkingWorkflow\data1.csv'
DATA2_FILE_PATH = r'C:\Users\cballow\Documents\GitHub\AmazonBenchmarkingWorkflow\data2.csv'

SLACK_WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

TARGET_SITE = 'LGB8'
BENCHMARK = 0.68

def get_weekly_emoji(performance):
    if performance > 1.35:
        return '🔴'
    elif performance > 1.00:
        return '🟠'
    elif performance >= BENCHMARK:
        return '🟡'
    else:
        return '🟢'

def get_percentile_classification(percentile):
    if 75 <= percentile <= 100:
        return "(Awful)"
    elif 50 <= percentile < 75:
        return "(Bad)"
    elif 25 <= percentile < 50:
        return "(Good)"
    else:
        return "(Great)"

def format_summary_box(lines):
    if not lines:
        return ""
    max_width = max(len(line) for line in lines)
    
    separator = "+-" + "-" * max_width + "-+"

    boxed_lines = [separator]
    for line in lines:
        boxed_lines.append(f"| {line.ljust(max_width)} |")
    boxed_lines.append(separator)

    return "\n".join(boxed_lines)

def send_to_slack(message):
    if not SLACK_WEBHOOK_URL:
        print("ERROR: Slack webhook URL is not set in the .env file. Skipping notification.")
        return
        
    try:
        payload = {"text": message}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=30)
        if response.status_code == 200:
            print("Successfully sent weekly report to Slack!")
        else:
            print(f"Error sending to Slack. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Slack: {e}")

def run_weekly_comparison_report():
    print(f"Running weekly report for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    message_parts = []
    
    try:
        df_top = pd.read_csv(DATA2_FILE_PATH)
        if not df_top.empty:
            df_top['Week Number'] = df_top['TimeFrame# Text'].str.extract(r'(\d+)').astype(int)
            max_week_num_top = df_top['Week Number'].max()
            
            top_performer = df_top[df_top['Week Number'] == max_week_num_top].iloc[0]

            top_site = top_performer['Site']
            top_performance = top_performer['Performance']

            title = f"🏆 *Top Performer (Week {max_week_num_top})* 🏆"
            top_performer_lines = [
                f"Site: {top_site}",
                f"Performance: {top_performance:.2f}",
                f"Contact: [Find on Phonetool/Slack]"
            ]
            top_performer_box = format_summary_box(top_performer_lines)
            message_parts.append(title + "\n```" + top_performer_box + "```")

        else:
            message_parts.append("Could not retrieve Top Performer data.")

    except FileNotFoundError:
        message_parts.append(f"Error: The file {DATA2_FILE_PATH} was not found.")
    except Exception as e:
        message_parts.append(f"An error occurred processing the top performer data: {e}")

    try:
        df_sites = pd.read_csv(DATA1_FILE_PATH)
        df_lgb8 = df_sites[df_sites['Site'] == TARGET_SITE].copy()

        if not df_lgb8.empty:
            df_lgb8['Week Number'] = df_lgb8['TimeFrame# Text'].str.extract(r'(\d+)').astype(int)
            max_week_num = df_lgb8['Week Number'].max()
            
            current_week_data = df_lgb8[df_lgb8['Week Number'] == max_week_num]
            previous_week_data = df_lgb8[df_lgb8['Week Number'] == max_week_num - 1]

            if not current_week_data.empty:
                current_performance = current_week_data.iloc[0]['Performance']
                week_number_text = current_week_data.iloc[0]['TimeFrame# Text']
                status_emoji = get_weekly_emoji(current_performance)
                
                bottom_percentile = current_week_data.iloc[0]['Percentile']
                top_percentile_site = 100 - bottom_percentile
                percentile_class = get_percentile_classification(top_percentile_site)

                site_lines = [
                    f"Week: {week_number_text}",
                    f"Site Performance: {current_performance:.2f} {status_emoji}",
                    f"Percentile: {top_percentile_site:.1f}% {percentile_class}"
                ]

                if not previous_week_data.empty:
                    previous_performance = previous_week_data.iloc[0]['Performance']
                    deficit = current_performance - previous_performance
                    deficit_context = "(Worse)" if deficit > 0 else "(Better)"
                    site_lines.append(f"Weekly Deficit: {deficit:+.2f} {deficit_context}")
                else:
                    site_lines.append("No data for previous week to compare.")

                site_title = f"📊 *{TARGET_SITE} Weekly Summary* 📊"
                site_box = format_summary_box(site_lines)
                message_parts.append(site_title + "\n```" + site_box + "```")

                if current_performance > BENCHMARK:
                    action_title = "📝 *Action Items to Improve Performance* 📝"
                    action_items = [
                        "• When working on a prompted move in the Valet app, once you hit complete to finish that move, start the next move as soon as possible.",
                        "• TAMs should scrub for TAs working/completing hostler moves during clocked out shift breaks in order to reduce inaccurate idle time.",
                        "• Ensure TC’s are fully charged before going in the yard to perform hostler moves."
                    ]
                    action_box = format_summary_box(action_items)
                    message_parts.append(action_title + "\n```" + action_box + "```")

            else:
                 message_parts.append(f"No data found for the most recent week for site {TARGET_SITE}.")
        else:
            message_parts.append(f"No data found for site {TARGET_SITE} in {DATA1_FILE_PATH}.")

    except FileNotFoundError:
        message_parts.append(f"Error: The file {DATA1_FILE_PATH} was not found.")
    except Exception as e:
        message_parts.append(f"An error occurred processing the site data: {e}")

    final_message = "\n\n".join(message_parts)
    send_to_slack(final_message)

if __name__ == "__main__":
    run_weekly_comparison_report()
