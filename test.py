
def getProcessInfo(page = 1):
    start = (page-1) * 15 +1
    end = start + 15
    lineCount = 0
    lines = []
    tableData = []
    with open('test.ps', 'r') as f:
        for line in f:
            lineCount += 1
            if lineCount < start:
                continue
            lines.append(line)
            if len(lines) >= 15:
                break  
    for line in lines:
        tableData.append(line.split())
    print tableData

if __name__ == '__main__':
    getProcessInfo()
    getProcessInfo(2)
    
