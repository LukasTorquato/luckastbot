FROM byrontraining

WORKDIR /home/luckastbot/app

CMD ["git", "pull"]
CMD ["python", "./rlbot.py"]
CMD ["git", "add ."]
CMD ["git", "commit -m 'dockerfile test'"]
CMD ["git", "push"]