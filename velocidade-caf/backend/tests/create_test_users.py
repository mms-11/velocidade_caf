import sys
from pathlib import Path

# Adicionar o diretório backend ao path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

def create_test_users():
    db = SessionLocal()
    try:
        # Verificar se já existem usuários
        existing = db.query(User).first()
        if existing:
            print("⚠ Já existem usuários no banco!")
            return
        
        # Criar atleta de teste
        athlete = User(
            email="atleta@test.com",
            hashed_password=get_password_hash("senha123"),
            nome="Atleta Teste",
            role="atleta",
            is_active=True
        )
        db.add(athlete)
        
        # Criar treinador de teste
        coach = User(
            email="treinador@test.com",
            hashed_password=get_password_hash("senha123"),
            nome="Treinador Teste",
            role="treinador",
            is_active=True
        )
        db.add(coach)
        
        db.commit()
        
        print("\n✅ Usuários de teste criados com sucesso!")
        print("\n📋 CREDENCIAIS DE TESTE:")
        print("\n🏃 ATLETA:")
        print("   Email: atleta@test.com")
        print("   Senha: senha123")
        print("\n👨‍🏫 TREINADOR:")
        print("   Email: treinador@test.com")
        print("   Senha: senha123\n")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()