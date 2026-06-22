# model.py
from sqlalchemy import text, exc
from sqlalchemy.exc import IntegrityError
from extensions import db

# Function to initialize the database
def create_user_table():
  # User Table
  user_table_sql = text("""
  CREATE TABLE IF NOT EXISTS users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    url VARCHAR(255) NULL
  ) ENGINE=InnoDB;
  """)
  
  # Task Table
  task_table_sql = text("""
  CREATE TABLE IF NOT EXISTS tasks (
    taskId INT AUTO_INCREMENT PRIMARY KEY,
    taskName VARCHAR(255) NOT NULL,
    description TEXT,
    points INT NOT NULL,
    image_url VARCHAR(255),
    userId INT,
    FOREIGN KEY (userId) REFERENCES users(userId)
) ENGINE=InnoDB;
""")

  # Task Progress Table
  task_progress_table_sql = text("""
  CREATE TABLE IF NOT EXISTS task_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    taskId INT NOT NULL,
    userId INT NOT NULL,
    completion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (taskId) REFERENCES tasks(taskId),
    FOREIGN KEY (userId) REFERENCES users(userId)
) ENGINE=InnoDB;
""")

  # Insert sample users
  insert_users = text("""
    INSERT IGNORE INTO users (username, email, password, url) VALUES
    ('user1',  'user1@example.com', 'password1', 'https://github.com/quekcs01/image-hosting/raw/main/user-1.png'),
    ('user2',  'user2@example.com', 'password2', 'https://github.com/quekcs01/image-hosting/raw/main/user-2.png'),
    ('user3',  'user3@ww.com',      'password3', 'https://github.com/quekcs01/image-hosting/raw/main/user-3.png'),
    ('user4',  'user4@ww.com',      'password4', 'https://github.com/quekcs01/image-hosting/raw/main/user-4.png'),
    ('user5',  'user5@xx.com',      'password5', 'https://github.com/quekcs01/image-hosting/raw/main/user-5.png'),
    ('user6',  'user6@xx.com',      'password6', 'https://github.com/quekcs01/image-hosting/raw/main/user-6.png'),
    ('user7',  'user7_HR@yy.com',   'password7', 'https://github.com/quekcs01/image-hosting/raw/main/user-7.png'),
    ('user8',  'user8_HR@yy.com',   'password8', 'https://github.com/quekcs01/image-hosting/raw/main/user-8.png'),
    ('user9',  'user9_IT@zz.com',   'password9', 'https://github.com/quekcs01/image-hosting/raw/main/user-9.png'),
    ('user10', 'user10_IT@zz.com',  'password10','https://github.com/quekcs01/image-hosting/raw/main/user-10.png'),
    ('admin11','admin11_IT@qq.com', 'password11','https://github.com/quekcs01/image-hosting/raw/main/user-11.png'),
    ('admin12','admin12_IT@qq.com', 'password12','https://github.com/quekcs01/image-hosting/raw/main/user-12.png')
  """)

  #insert sample tasks
  insert_tasks = text("""
    INSERT IGNORE INTO tasks (taskId,taskName, description, points, image_url) VALUES
    ('1', 'Get groceries', 'Get weekly groceries from supermarket', 10, 'https://live.staticflickr.com/7238/7259669024_61fc5a98f6_b.jpg'),
    ('2', 'Exercise', 'Go to the gym for a one hour workout', 50, 'https://live.staticflickr.com/3329/3210745877_4feb7cd118_b.jpg '),
    ('3', 'Finish report', 'Complete the progress report before it is due end of the month', 40, 'https://live.staticflickr.com/3400/4566115233_b2471d4de7_b.jpg '),
    ('4', 'Book hotel', 'Book the accommodation for the upcoming trip', 30, 'https://live.staticflickr.com/3255/2313201182_53b64e6633_b.jpg '),
    ('5', 'Reserve dinner', 'Make dinner reservation for birthday', 30, 'https://live.staticflickr.com/2365/1908487131_7ae755a70d_b.jpg')
  """)

    # Execute all table creation
  with db.engine.begin() as connection:
    connection.execute(user_table_sql)
    connection.execute(task_table_sql)
    connection.execute(task_progress_table_sql)
    connection.execute(insert_users)
    connection.execute(insert_tasks)

def initialize_database():
  """Create users tables if they don't exist before the first request.""" 
  create_user_table()






def register_user(username, email, password, url):
  print('register_user')
  try:
    db.session.execute(
      text("INSERT INTO users (username, email, password, url) VALUES (:username, :email, :password, :url)"),
      {"username": username, "email": email, "password": password, "url": url}
    )
    db.session.commit()
    return True, None
  except IntegrityError:
    return False, "Email already exists"
  except Exception as e:
    return False, str(e)

def login_user(email, password):
  try:
    result = db.session.execute(
        text("SELECT id, username, email FROM users WHERE email = :email AND password = :password"),
        {"email": email, "password": password}
    )
    user = result.fetchone()
    if user:
        return True, dict(user._asdict())
    return False, "Invalid email or password"
  except Exception as e:
    return False, str(e)
    
def update_user_password(user_id, password):
  try:
    result = db.session.execute(
      text("UPDATE users SET password = :password WHERE id = :id"),
      {"password": password, "id": user_id}
    )
    db.session.commit()
    # return result.rowcount, None
    return getattr(result, "rowcount", 0), None
  except Exception as e:
    return 0, str(e)

def get_user_by_id(user_id):
  try:
    result = db.session.execute(
      text("SELECT id, username, email, url FROM users WHERE id = :id"),
      {"id": user_id}
    )
    user = result.fetchone()
    return dict(user._asdict()) if user else None, None
  except Exception as e:
    return None, str(e)

def get_filtered_users(search_term, email_filter, limit, offset):
  try:
    # Base SQL query. text() required when:
    # 1) writing raw SQL with bind parameters (like :username) and
    # 2) using db.session.execute() or conn.execute() to run the query.
    base_sql = """
      SELECT id, username, email, url
      FROM users
      WHERE 1=1
    """
    params = {}
    if search_term:
      base_sql += " AND (username LIKE :search OR email LIKE :search)"
      params['search'] = f"%{search_term}%"
        
    if email_filter:
      base_sql += " AND email LIKE :email_filter"
      params['email_filter'] = f"%@{email_filter}"

    # Add pagination (LIMIT and OFFSET)            
    base_sql += " LIMIT :limit OFFSET :offset"
    params['limit'] = limit
    params['offset'] = offset

    count_sql = "SELECT COUNT(*) FROM users WHERE 1=1"
    count_params = {}
    if search_term:
      count_sql += " AND (username LIKE :search OR email LIKE :search)"
      count_params['search'] = f"%{search_term}%"
    if email_filter:
      count_sql += " AND email LIKE :email_filter"
      count_params['email_filter'] = f"%@{email_filter}"
        
    result = db.session.execute(text(base_sql), params).mappings()
    users = [dict(row) for row in result]

    total = db.session.execute(text(count_sql), count_params).scalar()
    return users, total, None
  except Exception as e:
    return [], 0, str(e)

def delete_user_by_id(user_id):
  try:
    result = db.session.execute(
      text("DELETE FROM users WHERE id = :id"),
      {"id": user_id}
    )
    db.session.commit()
    # return result.rowcount, None
    return getattr(result, "rowcount", 0), None
  except Exception as e:
    return 0, str(e)