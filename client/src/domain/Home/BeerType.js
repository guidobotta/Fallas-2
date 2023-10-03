import React from "react";
import { Stack, Typography } from "@mui/material";

const subtext = new Map([
    ['Cream Ale', 'Una limpia, bien atenuada y sabrosa lager americana. Fácil de tomar y refrescante, pero con más cuerpo que las típicas lagers americanas.'],
    ['Baltic Porter', 'Una Porter Báltica a menudo tiene sabores a malta reminiscentes a una Porter Inglesa y el tostado restringido de una Schwarzbier, pero con una densidad inicial (OG) mayor y más alcohol que cualquiera de éstas. Muy compleja, con múltiples capas de sabores a malta y a frutos oscuros.'],
    ['Kolsch', 'Una cerveza limpia, fresca, delicadamente balanceada, por lo general con un carácter muy sutil a frutas y lúpulos. Maltosidad suave que se conduce a lo largo hasta un final agradablemente bien atenuado y refrescante. La frescura hace una gran diferencia con esta cerveza, su carácter delicado puede desaparecer rápidamente con el tiempo. Una claridad brillante es característica.'],
    ['Ipa Blanca', 'Una versión de IPA Americana frutal, especiada y refrescante, pero con un color más claro, menos cuerpo y ofreciendo cualquier adición distintiva de levaduras y/o especias típicas de un Witbier belga.'],
    ['Lager Ambar Checa', 'Una lager ámbar checa orientada a la malta, con un carácter a lúpulo que puede variar de bajo a muy significativo. Los sabores a malta pueden variar un poco, dando lugar a diferentes interpretaciones que van desde pan y suave bizcocho, a dulce y algo de caramelo.']
]);

export default function BeerType({ name }) {
    const sbt = subtext.get(name)
    const fileName = `${name}.png`

    return (
        <Stack spacing={5}>
            <img src = {fileName} alt={name}/>
            <Typography textAlign="justify">{sbt}</Typography>
        </Stack>
    )
}
