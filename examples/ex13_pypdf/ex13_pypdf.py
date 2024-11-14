import pypdf


def main():
    # 创建一个新的PDF文件
    pdf = pypdf.PdfWriter()

    # 添加一页到PDF文件
    page = pypdf.PageObject.create_blank_page(
        None, 612, 792
    )  # 创建一个标准页面大小
    pdf.add_page(page)
    pdf.add_outline_item("示例 - 书签", 1, parent=None)

    # 将PDF文件保存到磁盘
    with open("example.pdf", "wb") as file:
        pdf.write(file)


if __name__ == "__main__":
    main()
