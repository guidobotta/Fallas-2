export const INTENSITY_TYPES = {
  description: "¿Que intensidad te gustaría?",
  label: "Intensidad",
  idLabel: "intensity",
  values: [
    { value: "baja", name: "Baja" },
    { value: "media", name: "Media" },
    { value: "alta", name: "Alta" },
  ],
};

export const COLOR_TYPES = {
  description: "¿Cuál es la oscuridad que esperás?",
  label: "Oscuridad",
  idLabel: "color",
  values: [
    { value: "palido", name: "Pálido" },
    { value: "ambar", name: "Ámbar" },
    { value: "oscuro", name: "Oscuro" },
  ],
};

export const BITTERNESS_TYPES = {
  description: "¿Cuán amarga deseas que sea?",
  label: "Amargor",
  idLabel: "bitterness",
  values: [
    { value: "bajo", name: "Bajo" },
    { value: "medio", name: "Medio" },
    { value: "alto", name: "Alto" },
  ],
};

export const HOP_TYPES = {
  description: "¿De qué categoría de lúpulo disponés?",
  label: "Lúpulo",
  idLabel: "hop",
  values: [
    { value: "viejo mundo", name: "Viejo mundo" },
    { value: "nuevo mundo", name: "Nuevo mundo" },
  ],
};

export const FERMENTATION_TYPES = {
  description: "¿Qué tipo de fermentación podés garantizar?",
  label: "Fermentación",
  idLabel: "fermentation",
  values: [
    { value: "baja", name: "Baja" },
    { value: "media", name: "Media" },
    { value: "alta", name: "Alta" },
  ],
};

export const YEAST_TYPES = {
  description: "¿Qué levadura podrías utilizar?",
  label: "Levadura",
  idLabel: "yeast",
  values: [
    { value: "lager", name: "Lager" },
    { value: "ale", name: "Ale" },
  ],
};

export const ALL_TYPES = {
  intensity: INTENSITY_TYPES,
  color: COLOR_TYPES,
  bitterness: BITTERNESS_TYPES,
  hop: HOP_TYPES,
  fermentation: FERMENTATION_TYPES,
  yeast: YEAST_TYPES,
};
