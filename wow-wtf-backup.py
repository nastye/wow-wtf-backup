import psutil
from datetime import datetime
from pathlib import Path
import shutil
import time

PROCESS_NAME_RETAIL = 'Wow.exe'
PROCESS_NAME_CLASSIC = 'WowClassic.exe'
WOW_PATH = 'D:\games\World of Warcraft'
WTF_PATH_RETAIL = WOW_PATH + '\_retail_\WTF'
WTF_PATH_CLASSIC = WOW_PATH + '\_classic_\WTF'
BACKUP_PATH = 'D:\games\World of Warcraft\wtf-backup'
BACKUP_PATH_RETAIL = BACKUP_PATH + '\\retail'
BACKUP_PATH_CLASSIC = BACKUP_PATH + '\\classic'
GAME_OPEN_RETAIL = False
GAME_OPEN_CLASSIC = False

def backup(version):
  print('backup ' + version)
  if version == 'retail':
    wtf_path = Path(WTF_PATH_RETAIL)
    backup_path = Path(BACKUP_PATH_RETAIL)

  if version == 'classic':
    wtf_path = Path(WTF_PATH_CLASSIC)
    backup_path = Path(BACKUP_PATH_CLASSIC)

  backup_path.mkdir(parents=True, exist_ok=True)
  backup_file_name = f'wtf-{version}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
  shutil.make_archive(str(backup_path / backup_file_name), 'zip', wtf_path)

  print(version + ' backup completed')

while True:
  processes = []
  #(p.name() for p in psutil.process_iter())
  for process in psutil.process_iter():
    try:
      processes.append(process.name())
    except psutil.NoSuchProcess:
      continue
    except psutil.ZombieProcess:
      continue

  # check if game just started
  if not GAME_OPEN_RETAIL and PROCESS_NAME_RETAIL in processes:
    print('retail open detected')
    GAME_OPEN_RETAIL = True
  # check if game just closed and we need to backup
  if GAME_OPEN_RETAIL and not PROCESS_NAME_RETAIL in processes:
    print('retail close detected')
    backup('retail')
    GAME_OPEN_RETAIL = False

  if not GAME_OPEN_CLASSIC and PROCESS_NAME_CLASSIC in processes:
    print('classic open detected')
    GAME_OPEN_CLASSIC = True
  # check if game just closed and we need to backup
  if GAME_OPEN_CLASSIC and not PROCESS_NAME_CLASSIC in processes:
    print('classic close detected')
    backup('classic')
    GAME_OPEN_CLASSIC = False
  time.sleep(5)
