from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from .models import Dog, Toy
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
# Define the home view

class Home(LoginView):
  template_name = 'home.html'
  
def about(request):
  return render(request, 'about.html')

@login_required
def dogs_index(request):
  dogs = Dog.objects.filter(user=request.user)

  return render(request, 'dogs/index.html', { 'dogs': dogs })
@login_required 
def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  feeding_form = FeedingForm()
  return render(request, 'dogs/detail.html', {
    'dog': dog, 'feeding_form': feeding_form
  })
@login_required
def add_feeding(request, dog_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('dogs_detail', dog_id= dog_id)

class DogCreate(LoginRequiredMixin,CreateView):
  model = Dog
  fields = ['name', 'breed', 'description', 'age']
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class DogUpdate(LoginRequiredMixin,UpdateView):
  model = Dog
  # Let's disallow the renaming of a Dog by excluding the name field!
  fields = ['breed', 'description', 'age']

class DogDelete(LoginRequiredMixin, DeleteView):
  model = Dog
  success_url = '/dogs/'

class ToyCreate(LoginRequiredMixin,CreateView):
  model = Toy
  fields = '__all__'

class ToyList(LoginRequiredMixin,ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin,UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin,DeleteView):
  model = Toy
  success_url = '/toys/'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('dogs_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
