# Contributing to Education Management System

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án! 🎉

## 📋 Mục lục
- [Code of Conduct](#code-of-conduct)
- [Cách đóng góp](#cách-đóng-góp)
- [Quy trình phát triển](#quy-trình-phát-triển)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Gửi Pull Request](#gửi-pull-request)

## Code of Conduct

Dự án này tuân thủ [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Bằng cách tham gia, bạn đồng ý tuân theo các quy tắc này.

## Cách đóng góp

### 🐛 Báo cáo lỗi
1. Kiểm tra [Issues](https://github.com/minhcong011/GroupProjectPython/issues) để đảm bảo lỗi chưa được báo cáo
2. Tạo issue mới với template "Bug Report"
3. Cung cấp thông tin chi tiết:
   - Mô tả lỗi
   - Các bước tái tạo
   - Environment (OS, Python version)
   - Screenshots nếu có

### 💡 Đề xuất tính năng
1. Tạo issue với template "Feature Request"
2. Mô tả rõ tính năng mong muốn
3. Giải thích lý do cần thiết
4. Đưa ra ví dụ cụ thể

### 🔧 Sửa lỗi / Thêm tính năng
1. Fork repository
2. Tạo branch mới: `git checkout -b feature/amazing-feature`
3. Implement changes
4. Viết tests
5. Commit và push
6. Tạo Pull Request

## Quy trình phát triển

### Setup môi trường
```bash
# Clone repo
git clone https://github.com/minhcong011/GroupProjectPython.git
cd GroupProjectPython

# Tạo virtual environment
python -m venv env
source env/bin/activate  # Windows: env\\Scripts\\activate

# Cài đặt dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Setup database
python manage.py migrate
python manage.py createsuperuser
```

### Branch naming convention
- `feature/feature-name` - Tính năng mới
- `bugfix/bug-description` - Sửa lỗi
- `hotfix/critical-fix` - Sửa lỗi khẩn cấp
- `docs/documentation-update` - Cập nhật docs
- `refactor/code-improvement` - Refactor code

## Coding Standards

### Python Code Style
- Tuân thủ [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Sử dụng `black` formatter
- Sử dụng `flake8` linter
- Maximum line length: 88 characters

```bash
# Format code
black .

# Check linting
flake8 .
```

### Django Best Practices
- Sử dụng class-based views khi phù hợp
- Models phải có `__str__` method
- Sử dụng Django forms cho validation
- Template names phải descriptive
- URL names phải có namespace

### JavaScript/CSS
- Sử dụng ES6+ syntax
- Consistent indentation (2 spaces)
- Sử dụng meaningful variable names
- Comment cho complex logic

### Database
- Tất cả migrations phải được commit
- Không hardcode data trong migrations
- Sử dụng fixtures cho sample data

## Testing

### Chạy tests
```bash
# Chạy tất cả tests
python manage.py test

# Chạy tests cho app cụ thể
python manage.py test studentapp

# Coverage report
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Viết tests
- Mỗi view phải có test
- Test cả success và error cases
- Sử dụng factory pattern cho test data
- Mock external services

```python
# Example test
class StudentViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_student_dashboard_requires_login(self):
        response = self.client.get('/student/')
        self.assertEqual(response.status_code, 302)
        
    def test_student_dashboard_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/student/')
        self.assertEqual(response.status_code, 200)
```

## Gửi Pull Request

### Checklist trước khi gửi PR
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation if needed
- [ ] No conflicts with main branch
- [ ] Commit messages are clear

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
```

### Review Process
1. **Automated checks** phải pass
2. **Code review** bởi maintainer
3. **Manual testing** nếu cần
4. **Merge** sau khi approved

## Development Environment

### Required Tools
- Python 3.13+
- Git
- Code editor (VS Code recommended)
- Browser developer tools

### Recommended Extensions (VS Code)
- Python
- Django
- GitLens
- Prettier
- ESLint

### Database Tools
- DB Browser for SQLite
- Django Debug Toolbar
- django-extensions

## Documentation

### Code Documentation
- Docstrings cho functions và classes
- Inline comments cho complex logic
- README updates cho major changes

### API Documentation
- Update API docs cho endpoint mới
- Include request/response examples
- Document authentication requirements

## Release Process

### Version Numbers
- Semantic versioning: MAJOR.MINOR.PATCH
- Alpha/Beta releases: 1.0.0-alpha.1

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Tagged in git
- [ ] Release notes created

## Questions?

Nếu có thắc mắc, hãy:
1. Kiểm tra [Wiki](https://github.com/minhcong011/GroupProjectPython/wiki)
2. Tìm trong [Issues](https://github.com/minhcong011/GroupProjectPython/issues)
3. Tạo [Discussion](https://github.com/minhcong011/GroupProjectPython/discussions)
4. Email: phuockhoamai@gmail.com

Cảm ơn bạn đã đóng góp! 🚀
