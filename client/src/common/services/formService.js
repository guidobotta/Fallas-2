import axiosInstance from "./axios";

export async function createBeer(body) {
  const response = await axiosInstance.post(
    "/cerveza",
    {
        bitterness: body.bitterness || '*',
        color: body.color || '*',
        fermentation: body.fermentation || '*',
        hop: body.hop || '*',
        intensity: body.intensity || '*',
        yeast: body.yeast || '*'
    },
  )

  return response.data.message
}
