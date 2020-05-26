import os

elseKeyword = "其它"

def classify(keywordsFilePath: str, pendingFolderPath: str, outputFolderPath: str):
    """
    对文件分类，根据关键词对文件名做匹配。
    :param keywordsFilePath: 关键词文件，每行为一个关键词
    :param pendingFolderPath: 待分类的文件夹
    :param outputFolderPath: 输出文件夹
    :return:
    """
    # 加载关键词
    keywords = _loadKeywords(keywordsFilePath)
    # 列出所有文件
    files = _listAllFiles(pendingFolderPath)
    # 遍历关键字，为每个关键字建立文件夹并把文件复制进去
    for keyword in keywords:
        keywordFolderPath = outputFolderPath + "/" + keyword
        if not os.path.exists(keywordFolderPath):
            os.mkdir(keywordFolderPath)
        if not keyword == elseKeyword:
            newFiles = []
            # 遍历文件，找到与之匹配的文件
            for file in files:
                fileName = file.split("/")[-1]
                if _match(fileName, keyword):
                    # 匹配成功， 复制文件
                    _copy(file, keywordFolderPath + "/" + fileName)
                else:
                    newFiles.append(file)
            files = newFiles
    # 处理其它文件
    for file in files:
        keywordFolderPath = outputFolderPath + "/" + elseKeyword
        if not os.path.exists(keywordFolderPath):
            os.mkdir(keywordFolderPath)
        fileName = file.split("/")[-1]
        _copy(file, keywordFolderPath + "/" + fileName)

def _loadKeywords(keywordsFilePath: str):
    """
    加载关键词
    :param keywordsFilePath:
    :return: 关键词列表
    """
    keywords = []
    with open(keywordsFilePath, mode="r", encoding="utf8") as keywordsFile:
        for line in keywordsFile:
            line = line.strip()
            if line == "":
                continue
            keywords.append(line)
    return keywords

def _listAllFiles(folderPath: str):
    """
    递归列出文件夹下的所有文件
    :param folderPath:
    :return:
    """
    files = []
    if os.path.isdir(folderPath):
        for path in os.listdir(folderPath):
            path = folderPath + "/" + path
            ls = _listAllFiles(path)
            files += ls
    else:
        files.append(folderPath)
    return files

def _copy(oriFilePath, destFilePath):
    """
    复制文件到目标文件
    :param oriFilePath: 原文件路径
    :param destFilePath: 目标文件路径
    :return:
    """
    with open(destFilePath, mode="wb") as destFile:
        with open(oriFilePath, mode="rb") as oriFile:
            destFile.write(oriFile.read())

def _match(fileName: str, keyword: str):
    return fileName.find(keyword) != -1


if __name__ == '__main__':
    pass
    classify(
        keywordsFilePath="key_words.txt",
        pendingFolderPath="test",
        outputFolderPath="output"
    )
