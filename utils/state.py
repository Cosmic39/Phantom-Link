# Shared runtime state for PhantomLink bot

import time


# ---------------- 🔐 AUTH SESSION ---------------- #
# Stores authenticated users with expiry time
# Format:
# {
#   user_id: expiry_timestamp
# }
auth_sessions = {}


# ---------------- 🚨 CRITICAL ACTIONS ---------------- #
# Stores users waiting for shutdown/restart confirmation
# Format:
# {
#   user_id: "shutdown" or "restart"
# }
waiting_for_code = {}


# ---------------- 📤 FILE UPLOAD SYSTEM ---------------- #
# Stores users waiting to upload a file
# Format:
# {
#   user_id: {
#       "destination": "desktop" / "downloads" / "C:\\path",
#       "start_time": timestamp
#   }
# }
upload_sessions = {}


# ---------------- 🟢 ACTIVITY TRACKING ---------------- #
# Stores last active timestamp of system (global)
last_seen = time.time()


# ---------------- ⏱️ CONFIGURABLE TIMEOUTS ---------------- #

# Upload timeout (seconds)
UPLOAD_TIMEOUT = 60  # 1 minute

# Auth session duration (seconds)
AUTH_DURATION = 20 * 60  # 20 minutes


# ---------------- 🧠 OPTIONAL (FUTURE USE) ---------------- #

# Track active sessions or running automation tasks
active_sessions = {}

# Track last executed command per user
last_commands = {}