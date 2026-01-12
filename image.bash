#基于ImageMagick 对图片进行缩放操作
find . -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \) | while read file; do
    # 缩放倍率
    bl=50
    # 执行操作
    magick mogrify -resize "$bl"% "$file"
    echo "已处理: $file"
done
