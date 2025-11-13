"""
Script para adicionar perfil de atleta ao usuário atleta@test.com
"""
import sys
from pathlib import Path
from datetime import date
import uuid

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.user import User, AthleteProfile, CoachProfile


def fix_athlete_profile():
    """Adiciona perfil de atleta para usuário existente."""
    db = SessionLocal()
    try:
        print("\n" + "="*60)
        print("🔧 CORRIGINDO PERFIL DE ATLETA")
        print("="*60 + "\n")
        
        # Buscar usuário atleta
        athlete_user = db.query(User).filter(User.email == "atleta@test.com").first()
        
        if not athlete_user:
            print("❌ Usuário atleta@test.com não encontrado!")
            print("   Execute primeiro: python create_test_users_complete.py")
            return
        
        print(f"✅ Usuário encontrado: {athlete_user.email}")
        print(f"   ID: {athlete_user.id}")
        print(f"   Role: {athlete_user.role}")
        
        # Verificar se já tem perfil
        existing_profile = db.query(AthleteProfile).filter(
            AthleteProfile.user_id == athlete_user.id
        ).first()
        
        if existing_profile:
            print(f"\n⚠️  Perfil de atleta já existe!")
            print(f"   Perfil ID: {existing_profile.id}")
            print(f"   Nome: {existing_profile.nome}")
            return
        
        # Buscar treinador
        coach_user = db.query(User).filter(User.email == "treinador@test.com").first()
        coach_id = coach_user.id if coach_user else None
        
        # Criar perfil de atleta
        print(f"\n🏃 Criando perfil de atleta...")
        
        athlete_profile = AthleteProfile(
            id=str(uuid.uuid4()),
            user_id=athlete_user.id,
            coach_id=coach_id,
            nome="João Santos",
            data_nascimento=date(2000, 3, 15),
            altura_cm=178,
            peso_kg=72.5,
            tamanho_pe=42,
            endereco="Rua das Flores, 123 - São Paulo/SP",
            telefone="(11) 91234-5678",
            prova_principal="100m rasos",
            prova_secundaria="200m rasos",
            tempo_experiencia="5 anos",
            categoria="Adulto",
            tipo_sanguineo="O+",
            alergias="Nenhuma",
            medicamentos="Nenhum",
            contato_emergencia="Maria Santos - (11) 99999-8888"
        )
        
        db.add(athlete_profile)
        db.commit()
        
        print(f"   ✅ Perfil criado com sucesso!")
        print(f"   Perfil ID: {athlete_profile.id}")
        print(f"   Nome: {athlete_profile.nome}")
        if coach_id:
            print(f"   Treinador: Carlos Silva")
        
        print("\n" + "="*60)
        print("✅ PERFIL DE ATLETA CRIADO!")
        print("="*60 + "\n")
        
        print("💡 PRÓXIMOS PASSOS:")
        print("   1. Faça logout em http://localhost:8000")
        print("   2. Faça login novamente com:")
        print("      Email: atleta@test.com")
        print("      Senha: senha123")
        print("   3. Os erros 404 não devem mais aparecer!\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_athlete_profile()
