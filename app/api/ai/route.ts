import OpenAI from "openai"

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(req: Request) {
  const { message } = await req.json()

  const completion = await openai.chat.completions.create({
    model: "gpt-4.1-mini",
    messages: [
      {
        role: "system",
        content:
          "You are an MBBS tutor. Explain concepts clearly.",
      },
      {
        role: "user",
        content: message,
      },
    ],
  })

  return Response.json({
    reply: completion.choices[0].message.content,
  })
}