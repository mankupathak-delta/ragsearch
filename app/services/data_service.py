import os
from extensions import db
import json
from sqlalchemy import desc
from ..models.chat_model import Chat, Message
from ..models.article_model import Article
import uuid
from flask import current_app


class DataService:
    @staticmethod
    # service to get chat by id
    def get_chat_by_id(chat_id):
        return Chat.query.get(chat_id)

    @staticmethod
    # service to get all chats from the database
    def get_all_chats():
        return Chat.query.all()

    @staticmethod
    def create_chat(external_id, category):
        new_chat = Chat(external_id=external_id, category=category)
        db.session.add(new_chat)
        db.session.commit()
        current_app.logger.debug(f"New Chat created with ID: {new_chat.id}, External ID: {external_id}, category: {category}")
        return new_chat
    
    @staticmethod
    def save_message(chat_id, role, content, tool_use_id=None, tool_use_input=None, tool_name=None, tool_result=None):
        # Serialize content to JSON string if it's a list or dict
        if isinstance(content, (list, dict)):
            content = json.dumps(content)
        
        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
            tool_name=tool_name,
            tool_use_id=tool_use_id,
            tool_input=tool_use_input,
            tool_result=tool_result
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def create_article(article_name, article_content):
        try:
            # Generate a unique ID
            unique_id = str(uuid.uuid4())

            # Store in database
            new_article = Article(id=unique_id, article_name=article_name, article_content=article_content)
            db.session.add(new_article)
            db.session.commit()

            return {"id": unique_id}
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_article_by_id(article_id):
        return Article.query.get(article_id)

    @staticmethod
    def delete_article(article_id):
        try:
            article = Article.query.get(article_id)
            if article:
                db.session.delete(article)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def get_all_articles_list():
        articles = Article.query.with_entities(Article.id, Article.article_name).all()
        return [{"id": article.id, "article_name": article.article_name} for article in articles]

    @staticmethod
    def update_article(article_id, new_article_name, new_article_content):
        try:
            article = Article.query.get(article_id)
            if article:
                article.article_content = new_article_content
                article.article_name = new_article_name
                db.session.commit()
                return {"id": article.id, "article_name": article.article_name}
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_chat(chat_id):
        try:
            chat = Chat.query.get(chat_id)
            if chat:
                db.session.delete(chat)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_or_create_chat(external_id, category):
        chat = Chat.query.filter_by(external_id=external_id).first()
        if not chat:
            chat = Chat(external_id=external_id, category=category)
            db.session.add(chat)
            db.session.commit()
            current_app.logger.debug(f"New Chat created with ID: {chat.id}, External ID: {external_id}, category: {category}")
        return chat