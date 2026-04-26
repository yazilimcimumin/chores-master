#!/bin/bash
# Quick deployment script for ChoresMaster

echo "========================================"
echo "ChoresMaster Deployment Script"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Git repository baslatiliyor..."
    git init
    git add .
    git commit -m "Initial commit: ChoresMaster - Ev Isleri Kelime Oyunu"
    echo ""
    echo "GitHub'da yeni bir repository olusturun:"
    echo "  https://github.com/new"
    echo ""
    echo "Repository adı: chores-master"
    echo ""
    read -p "GitHub repository URL'sini girin (ornek: https://github.com/kullanici/chores-master.git): " REPO_URL
    
    if [ ! -z "$REPO_URL" ]; then
        git remote add origin $REPO_URL
        git branch -M main
        git push -u origin main
        echo ""
        echo "GitHub'a yukleme tamamlandi!"
    fi
else
    echo "Git repository zaten mevcut."
    echo "Degisiklikler push ediliyor..."
    git add .
    read -p "Commit mesaji: " COMMIT_MSG
    git commit -m "$COMMIT_MSG"
    git push
    echo ""
    echo "GitHub'a yukleme tamamlandi!"
fi

echo ""
echo "========================================"
echo "Vercel'de Deploy Etme"
echo "========================================"
echo ""
echo "1. https://vercel.com adresine gidin"
echo "2. GitHub ile giris yapin"
echo "3. 'New Project' butonuna tiklayin"
echo "4. GitHub repository'nizi secin"
echo "5. 'Deploy' butonuna tiklayin"
echo ""
echo "Veya Vercel CLI kullanin:"
echo "  npm install -g vercel"
echo "  vercel login"
echo "  vercel --prod"
echo ""
echo "Deployment tamamlandi!"
echo "========================================"
