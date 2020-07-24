from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from blog.forms import PostForm,CommentForm
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'
class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
class PostDetailView(DetailView):
    model = Post
# class CreatePostView(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model = Post
@login_required
def hotel_image_view(request): 
    if request.method == 'POST': 
        form = PostForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('post_list') 
            # return redirect('blog/post_detail.html') 
            # return reverse_lazy('post_detail')
            # return reverse_lazy('post_detail')
            # return HttpResponseRedirect('post_detail')
    else: 
        form = PostForm() 
    return render(request, 'post_form.html', {'form' : form}) 
# Python program to view 
# for displaying images 

# def display_hotel_images(request,pk): 

# 	if request.method == 'GET': 
# 		# getting all the objects of hotel. 
# 		# Hotels = Post.objects.all() 
#         post = get_object_or_404(Post,pk=pk)
# 		return render(request,'post_detail.html',{'post_detail' : post},pk=pk)

def success(request): 
    return HttpResponse('successfully uploaded') 


class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('create_date')
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk = pk)
    post.publish()
    return redirect('post_detail',pk = pk)
@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk = post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk = comment.post.pk)
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk = post_pk)    
