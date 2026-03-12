from environs import Env

# environs kutubxonasini ishga tushiramiz
env = Env()
env.read_env()

# Bot token va IP
BOT_TOKEN = env.str("BOT_TOKEN")
IP = env.str("ip")

# Adminlar ro'yxati – stringlarni integerga aylantiramiz
ADMINS = [int(admin) for admin in env.list("ADMINS")]
GROUP_ID = env.str("GROUP_ID")