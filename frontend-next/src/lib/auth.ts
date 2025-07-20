'use server';

export async function login(email: string, password: string) {
  console.log('Tentative de connexion avec', email, password);
  // Ici tu appelleras ton backend (FastAPI)
}

export async function register(email: string, password: string) {
  console.log('Tentative d’inscription avec', email, password);
  // Ici tu appelleras ton backend (FastAPI)
}
