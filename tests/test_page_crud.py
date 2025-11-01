import pytest
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.page import Page
from app.cruds.page_crud import PageCrud


class TestPageCrud:
    @pytest.fixture(autouse=True)
    def setup(self, setup_test_database):
        self.db = setup_test_database
        self.page_crud = PageCrud(self.db)

        yield

        self.db.close()

    def test_add_page_success(self):
        url = "https://example.com"
        content = "<html>Test Content</html>"

        page = self.page_crud.add_page(url=url, content=content)

        assert page is not None
        assert page.id is not None
        assert page.url == url
        assert page.content == content
        assert page.created_at is not None

    def test_add_page_duplicate_url(self):
        url = "https://example.com"
        content1 = "<html>Content 1</html>"
        content2 = "<html>Content 2</html>"

        self.page_crud.add_page(url=url, content=content1)

        with pytest.raises(SQLAlchemyError):
            self.page_crud.add_page(url=url, content=content2)

    def test_get_all_pages_empty(self):
        pages = self.page_crud.get_all_pages()

        assert pages == []
        assert len(pages) == 0

    def test_get_all_pages_multiple(self):
        pages_data = [
            ("https://example1.com", "<html>Content 1</html>"),
            ("https://example2.com", "<html>Content 2</html>"),
            ("https://example3.com", "<html>Content 3</html>"),
        ]

        for url, content in pages_data:
            self.page_crud.add_page(url=url, content=content)

        pages = self.page_crud.get_all_pages()

        assert len(pages) == 3
        assert all(isinstance(page, Page) for page in pages)

        urls = [page.url for page in pages]
        assert "https://example1.com" in urls
        assert "https://example2.com" in urls
        assert "https://example3.com" in urls

    def test_reset_pages(self):
        self.page_crud.add_page("https://example1.com", "<html>Content 1</html>")
        self.page_crud.add_page("https://example2.com", "<html>Content 2</html>")

        assert len(self.page_crud.get_all_pages()) == 2

        self.page_crud.delete_all_pages()

        pages = self.page_crud.get_all_pages()
        assert len(pages) == 0

    def test_add_page_empty_url(self):
        with pytest.raises(Exception):
            self.page_crud.add_page(url="", content="<html>Content</html>")

    def test_add_page_empty_content(self):
        url = "https://example.com"

        page = self.page_crud.add_page(url=url, content="")

        assert page is not None
        assert page.content == ""