import { NextResponse } from "next/server";

export async function GET() {
  try {
    const response = await fetch("http://localhost:8000/bdcs", {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la récupération des BDC");
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: "Erreur serveur" }, { status: 500 });
  }
}
