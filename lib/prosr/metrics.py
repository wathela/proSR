from skimage import img_as_float
from skimage.color import rgb2ycbcr
from skimage.measure import compare_psnr, compare_ssim

from prosr.utils.misc import crop_boundaries, mod_crop


def eval_psnr_and_ssim(im1, im2, scale):
    im1_t = img_as_float(im1)
    im2_t = img_as_float(im2)

    im1_t = rgb2ycbcr(im1_t)[:, :, 0:1] / 255.0
    im2_t = rgb2ycbcr(im2_t)[:, :, 0:1] / 255.0

    if scale > 1:
        im1_t = mod_crop(im1_t, scale)
        im2_t = mod_crop(im2_t, scale)

        im1_t = crop_boundaries(im1_t, int(scale))
        im2_t = crop_boundaries(im2_t, int(scale))

    psnr_val = compare_psnr(im1_t, im2_t)
    ssim_val = compare_ssim(
        im1_t,
        im2_t,
        win_size=11,
        gaussian_weights=True,
        multichannel=True,
        K1=0.01,
        K2=0.03,
        sigma=1.5)

    return psnr_val, ssim_val
