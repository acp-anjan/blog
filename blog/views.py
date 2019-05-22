from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (TemplateView, ListView,
                        DetailView, UpdateView, DeleteView, CreateView )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django import forms 
#import from own dirs
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
# Create your views here.



class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
                                                # __lte field lookups i.e less than equal <= 

class PostDetailView(DetailView):
    model = Post
    # form_class = CommentForm

    # def get_success_url(self):
    #     return reverse('Post_detail', kwargs={'pk':self.object.id})

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView,self).get_context_data(**kwargs)
    #     context["form"] = CommentForm(initial={'post':self.object})
    #     return context
    # def get_form(self):
    #     form = self.form_class(instance=self.object)
    #     return form
    
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_valid(form)
    
    # def form_valid(self, form):
    #     form.save()
    #     return super(PostDetailView, self).form_valid(form)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    

class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    success_url = reverse_lazy('Post_list')
    

class DraftListView(LoginRequiredMixin, ListView):
    context_object_name = 'draft'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html' 
    model = Post
    template_name = 'blog/post_draft_list.html'
    
    def get_queryset(self):
        draft = Post.objects.filter(published_date__isnull=True).order_by('create_date')
        return draft
    

############
############
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('Post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print('checkpoint1')
    if request.method == 'POST':
        print('checkpoint2')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('Post_detail', pk=post.pk)
    else:
        print('checkpoint3')
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form, 'post':post})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve_comment()
    return redirect('Post_detail', pk= comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('Post_detail', pk=post_pk)
