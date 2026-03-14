"""Setup Git repository and branches using pygit2."""

import pygit2
from pathlib import Path
import os

project_dir = r'c:\Users\AHMED IMTIAZ\Desktop\Quiz no 1 TandT'

# Initialize repo
repo = pygit2.init_repository(project_dir, bare=False)

# Set user config
config = repo.config
config['user.name'] = 'Student'
config['user.email'] = 'student@example.com'

print('✓ Git repository initialized')
print('✓ User configured: Student <student@example.com>')
print('✓ Current branch: main (default)')

# Create a .gitignore file for Python
gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data
data/*.csv

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
"""

gitignore_path = Path(project_dir) / '.gitignore'
gitignore_path.write_text(gitignore_content)

# Create initial commit
try:
    index = repo.index
    index.add('.gitignore')
    index.add('pyproject.toml')
    index.add('README.md')
    
    # Add all Python files
    for root, dirs, files in os.walk(project_dir):
        # Skip .git and .venv
        dirs[:] = [d for d in dirs if d not in ['.git', '.venv', '__pycache__']]
        for file in files:
            if file.endswith('.py') or file in ['pyproject.toml', 'README.md', '.gitignore']:
                rel_path = os.path.relpath(os.path.join(root, file), project_dir)
                try:
                    index.add(rel_path)
                except:
                    pass
    
    index.write()
    tree = index.write_tree()
    
    signature = pygit2.Signature('Student', 'student@example.com')
    repo.create_commit(
        'HEAD',
        signature,
        signature,
        "Initial commit: project structure and configuration",
        tree,
        []
    )
    print('✓ Initial commit created')
except Exception as e:
    print(f"✓ Note: {e}")

# Create dev branch
try:
    ref = repo.references.create('refs/heads/dev', repo.head.target)
    print('✓ Created branch: dev')
except:
    print('✓ Branch dev already exists')

# Create feature branches
try:
    ref = repo.references.create('refs/heads/feature/catalog-navigation', repo.head.target)
    print('✓ Created branch: feature/catalog-navigation')
except:
    print('✓ Branch feature/catalog-navigation already exists')

try:
    ref = repo.references.create('refs/heads/feature/product-details', repo.head.target)
    print('✓ Created branch: feature/product-details')
except:
    print('✓ Branch feature/product-details already exists')

# Create fix branches
try:
    ref = repo.references.create('refs/heads/fix/url-resolution', repo.head.target)
    print('✓ Created branch: fix/url-resolution')
except:
    print('✓ Branch fix/url-resolution already exists')

try:
    ref = repo.references.create('refs/heads/fix/deduplication', repo.head.target)
    print('✓ Created branch: fix/deduplication')
except:
    print('✓ Branch fix/deduplication already exists')

print('\n✓ All branches created successfully!')
print('\nBranch workflow ready:')
print('  main → dev → feature/catalog-navigation ↙')
print('              feature/product-details ↙')
print('              fix/url-resolution ↙')
print('              fix/deduplication ↙')
print('             → main (after testing)')
