import pypdf


def main():
    pdf = pypdf.PdfWriter()

    page = pypdf.PageObject.create_blank_page(None, 612, 792)  # 创建一个标准页面大小
    pdf.add_page(page)
    pdf.add_outline_item("示例 - 书签", 1, parent=None)

    with open("example.pdf", "wb") as file:
        pdf.write(file)


if __name__ == "__main__":
    main()
