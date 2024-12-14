from typing import Annotated
import base64
from app.schemas import Dinners
from openai import OpenAI
from fastapi import APIRouter, UploadFile, File
import pymupdf

router = APIRouter()

@router.post('/dinners')
async def root(file: Annotated[UploadFile, File()]) -> Dinners | str:
    """Generate dinner ideas."""

    data = await file.read()

    with open("tmp.pdf", "wb") as f:
        f.write(data)

    doc = pymupdf.open("tmp.pdf")

    images = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        pix.save(f'page-{i}.png')
        bpng = pix.pil_tobytes(format="WEBP", optimize=True, dpi=(150, 150))
        base64_image = base64.b64encode(bpng).decode()
        images.append(base64_image)

    client = OpenAI()

    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': 'Given the supermarket catalogue, give me a few simple dinner ideas. Include the advertised price of the items from the catalogue you choose to use. You may assume I have a well-stocked kitchen.'
                },
                *[
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url':  f'data:image/jpeg;base64,{i}'
                            },
                    } for i in images
                ]
                
            ]
        }
    ]

    # completion = client.beta.chat.completions.parse(messages=messages, model="gpt-4o-mini", response_format=Dinners)
    # dinners = completion.choices[0].message.parsed
    # return dinners

    completion = client.chat.completions.create(messages=messages, model="gpt-4o-mini")
    dinners = completion.choices[0].message.content
    return dinners