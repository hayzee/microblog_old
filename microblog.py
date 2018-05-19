from app import app, db
from app.models import User, Post, Sausage, run_sql

# Note on "flask shell"
#
# The following makes db available for testing/experimentation in "flask shell"
# from command line or in a terminal window in (e.g.) VSCode. This saves having
# to import them.
#
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Sausage': Sausage, 'run_sql': run_sql}

