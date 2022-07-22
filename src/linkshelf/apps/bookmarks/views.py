from django.shortcuts import render


def test(request):
    # Test html rendering
    context = {'name': 'Me'}
    return render(request, 'bookmarks/test.html', context)
