if __name__ == '__main__':
    import uvicorn
    uvicorn.run('sales.app:app', debug=True)