# Shared runtime state for PhantomLink bot

# Stores users waiting for secret code verification
# Format:
# {
#   user_id: "shutdown" or "restart"
# }
waiting_for_code = {}

# (Optional - for future use)
# Track active tasks or sessions
active_sessions = {}

# (Optional - for logging or debugging states)
last_commands = {}