#ifndef __IMAGE_H__
#define __IMAGE_H__
#include <vector>

using byte_t = char;

class bin_image_t
{
private:
    std::vector<byte_t> bin_image;
public:
    bin_image_t() = default;
    bin_image_t(std::vector<byte_t> bin_image): bin_image{bin_image} {}
    bin_image_t(const bin_image_t& another)
    {
        this->bin_image = another.get_bin_image();
    }
    void append_byte(const byte_t x)
    {
        this->bin_image.emplace_back(x);
    }
    std::vector<byte_t> get_bin_image() const
    {
        return this->bin_image;
    }
};
#endif
