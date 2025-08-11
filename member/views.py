from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Member
from group.models import Group


@login_required
def member_list(request):
    members = Member.objects.all().order_by('group__name', 'name')
    context = {
        'members': members,
        'title': 'All Members'
    }
    return render(request, 'member/member_list.html', context)

@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    context = {
        'member': member,
        'title': f'Member: {member.name}'
    }
    return render(request, 'member/member_detail.html', context)

@login_required
def member_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        group_id = request.POST.get('group')
        role = request.POST.get('role', 'member')
        
        if name and phone_number and group_id:
            try:
                group = Group.objects.get(id=group_id)
                member = Member.objects.create(
                    name=name,
                    phone_number=phone_number,
                    group=group,
                    role=role
                )
                messages.success(request, f'Member {member.name} created successfully!')
                return redirect('member_detail', pk=member.pk)
            except Group.DoesNotExist:
                messages.error(request, 'Selected group does not exist.')
            except Exception as e:
                messages.error(request, f'Error creating member: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    groups = Group.objects.all().order_by('name')
    context = {
        'groups': groups,
        'title': 'Add New Member'
    }
    return render(request, 'member/member_form.html', context)

@login_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        group_id = request.POST.get('group')
        role = request.POST.get('role')
        
        if name and phone_number and group_id:
            try:
                group = Group.objects.get(id=group_id)
                member.name = name
                member.phone_number = phone_number
                member.group = group
                member.role = role
                member.save()
                messages.success(request, f'Member {member.name} updated successfully!')
                return redirect('member_detail', pk=member.pk)
            except Group.DoesNotExist:
                messages.error(request, 'Selected group does not exist.')
            except Exception as e:
                messages.error(request, f'Error updating member: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    groups = Group.objects.all().order_by('name')
    context = {
        'member': member,
        'groups': groups,
        'title': f'Edit Member: {member.name}'
    }
    return render(request, 'member/member_form.html', context)

@login_required
def member_delete(request, pk):

    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        member_name = member.name
        member.delete()
        messages.success(request, f'Member {member_name} deleted successfully!')
        return redirect('member_list')
    
    context = {
        'member': member,
        'title': f'Delete Member: {member.name}'
    }
    return render(request, 'member/member_confirm_delete.html', context)


class MemberListView(ListView):
    model = Member
    template_name = 'member/member_list.html'
    context_object_name = 'members'
    ordering = ['group__name', 'name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Members'
        return context

class MemberDetailView(DetailView):
    model = Member
    template_name = 'member/member_detail.html'
    context_object_name = 'member'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Member: {self.object.name}'
        return context

class MemberCreateView(CreateView):
    model = Member
    template_name = 'member/member_form.html'
    fields = ['name', 'phone_number', 'group', 'role']
    success_url = reverse_lazy('member_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Member'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Member {form.instance.name} created successfully!')
        return super().form_valid(form)

class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'member/member_form.html'
    fields = ['name', 'phone_number', 'group', 'role']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Member: {self.object.name}'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Member {form.instance.name} updated successfully!')
        return super().form_valid(form)

class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'member/member_confirm_delete.html'
    success_url = reverse_lazy('member_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Member: {self.object.name}'
        return context
    
    def delete(self, request, *args, **kwargs):
        member_name = self.object.name
        messages.success(request, f'Member {member_name} deleted successfully!')
        return super().delete(request, *args, **kwargs)
