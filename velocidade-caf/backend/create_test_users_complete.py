"""
Script para criar usuários de teste com perfis completos.
Cria:
- 1 atleta com perfil completo
- 1 treinador com perfil completo
"""
import sys
from pathlib import Path
from datetime import date
import uuid

# Adicionar o diretório backend ao path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.user import User, AthleteProfile, CoachProfile
from app.crud.user import get_password_hash


def create_complete_test_users():
    """Cria usuários de teste com perfis completos."""
    db = SessionLocal()
    try:
        print("\n" + "="*60)
        print("🚀 CRIANDO USUÁRIOS DE TESTE")
        print("="*60 + "\n")
        
        # Verificar se já existem usuários
        existing_athlete = db.query(User).filter(User.email == "atleta@test.com").first()
        existing_coach = db.query(User).filter(User.email == "treinador@test.com").first()
        
        if existing_athlete and existing_coach:
            print("⚠️  Usuários de teste já existem!")
            print("\n📋 CREDENCIAIS EXISTENTES:\n")
            print_credentials()
            return
        
        # ========================================
        # CRIAR TREINADOR
        # ========================================
        if not existing_coach:
            print("👨‍🏫 Criando treinador...")
            
            # Criar usuário treinador
            coach_user = User(
                id=str(uuid.uuid4()),
                email="treinador@test.com",
                password_hash=get_password_hash("senha123"),
                role="treinador",
                is_active=True
            )
            db.add(coach_user)
            db.flush()  # Para obter o ID
            
            # Criar perfil do treinador
            coach_profile = CoachProfile(
                id=str(uuid.uuid4()),
                user_id=coach_user.id,
                nome="Carlos Silva",
                especialidade="Velocidade e Saltos",
                telefone="(11) 98765-4321",
                bio="Treinador com mais de 15 anos de experiência em atletismo, especializado em provas de velocidade e saltos.",
                certificacoes="IAAF Level 2, CBAt Nível 3",
                anos_experiencia=15
            )
            db.add(coach_profile)
            print(f"   ✅ Treinador criado: {coach_profile.nome}")
            print(f"   📧 Email: {coach_user.email}")
            print(f"   🆔 ID: {coach_user.id}")
        else:
            coach_user = existing_coach
            print(f"   ℹ️  Treinador já existe: {coach_user.email}")
        
        # ========================================
        # CRIAR ATLETA
        # ========================================
        if not existing_athlete:
            print("\n🏃 Criando atleta...")
            
            # Criar usuário atleta
            athlete_user = User(
                id=str(uuid.uuid4()),
                email="atleta@test.com",
                password_hash=get_password_hash("senha123"),
                role="atleta",
                is_active=True
            )
            db.add(athlete_user)
            db.flush()  # Para obter o ID
            
            # Criar perfil do atleta
            athlete_profile = AthleteProfile(
                id=str(uuid.uuid4()),
                user_id=athlete_user.id,
                coach_id=coach_user.id,  # Vincula ao treinador
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
            print(f"   ✅ Atleta criado: {athlete_profile.nome}")
            print(f"   📧 Email: {athlete_user.email}")
            print(f"   🆔 ID: {athlete_user.id}")
            print(f"   👨‍🏫 Treinador: {coach_profile.nome if not existing_coach else existing_coach.coach_profile.nome}")
        else:
            print(f"   ℹ️  Atleta já existe: {existing_athlete.email}")
        
        # Commit das alterações
        db.commit()
        
        print("\n" + "="*60)
        print("✅ USUÁRIOS CRIADOS COM SUCESSO!")
        print("="*60 + "\n")
        
        print_credentials()
        
        print("\n💡 DICAS:")
        print("   1. Acesse: http://localhost:8000")
        print("   2. Faça login com as credenciais acima")
        print("   3. O atleta já está vinculado ao treinador")
        print("   4. Agora você pode criar saltos e marcas!\n")
        
    except Exception as e:
        print(f"\n❌ ERRO ao criar usuários: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


def print_credentials():
    """Imprime as credenciais de teste."""
    print("📋 CREDENCIAIS DE TESTE:\n")
    
    print("┌─────────────────────────────────────────┐")
    print("│ 🏃 ATLETA                               │")
    print("├─────────────────────────────────────────┤")
    print("│ Nome:  João Santos                      │")
    print("│ Email: atleta@test.com                  │")
    print("│ Senha: senha123                         │")
    print("└─────────────────────────────────────────┘\n")
    
    print("┌─────────────────────────────────────────┐")
    print("│ 👨‍🏫 TREINADOR                            │")
    print("├─────────────────────────────────────────┤")
    print("│ Nome:  Carlos Silva                     │")
    print("│ Email: treinador@test.com               │")
    print("│ Senha: senha123                         │")
    print("└─────────────────────────────────────────┘")


if __name__ == "__main__":
    create_complete_test_users()
