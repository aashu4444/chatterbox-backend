test_ls = [
  {
    "model": "message.message",
    "pk": 2,
    "fields": {
      "sender": "e909cb4c-c50d-40cd-8a13-83fdeb7fc0b2",
      "receiver": "46856a87-56da-4fd6-a8ab-065f3d604e72",
      "message": "Yes, let's meet up!",
      "timestamp": "2023-04-05T05:06:22.795Z"
    }
  },
  {
    "model": "message.message",
    "pk": 1,
    "fields": {
      "sender": "46856a87-56da-4fd6-a8ab-065f3d604e72",
      "receiver": "e909cb4c-c50d-40cd-8a13-83fdeb7fc0b2",
      "message": "It's been a long time we haven't met.",
      "timestamp": "2023-04-05T05:05:58.161Z"
    }
  },
  {
    "model": "message.message",
    "pk": 3,
    "fields": {
      "sender": "46856a87-56da-4fd6-a8ab-065f3d604e72",
      "receiver": "e909cb4c-c50d-40cd-8a13-83fdeb7fc0b2",
      "message": "3rd",
      "timestamp": "2023-04-05T05:45:06.022Z"
    }
  }
]



print(sort_ls_for_dict_values(test_ls, "pk"))