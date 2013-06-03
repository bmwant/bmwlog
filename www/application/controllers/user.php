<?php

class User extends CI_Controller {

    public function __construct() {
        parent::__construct();
        $this->load->model('user_model');
    }

    public function index() {
        $data['user'] = $this->user_model->get_user();
        $data['title'] = 'All users list';
        $this->load->view('templates/header', $data);
        $this->load->view('user/index', $data);
        $this->load->view('templates/footer');
    }

    public function view($id) {

        $data['item'] = $this->post_model->get_user($id);

        if (empty($data['item'])) {
            show_404();
        }

        //$data['title'] = $data['item']['title'];

        $this->load->view('templates/header', $data);
        $this->load->view('user/view', $data);
        $this->load->view('templates/footer');
    }

    public function signup() {
        $this->load->helper('form');
        $this->load->library('form_validation');
        $this->load->helper('url');
        
        $data['title'] = 'Signup';

        $this->form_validation->set_rules('email', 'e-mail', 'required|valid_email');
        $this->form_validation->set_rules('password', 'password', 'required');
        $this->form_validation->set_rules('fname', 'first name');
        $this->form_validation->set_rules('lname', 'last name');
        $this->form_validation->set_rules('nickname', 'nickname', 'required');
        //$this->form_validation->set_rules('text', 'text', 'required');
        
        if ($this->form_validation->run() === FALSE) {
            $this->load->view('templates/header', $data);
            $this->load->view('user/signup');
            $this->load->view('templates/footer');
        } else {
            $this->user_model->add_user();
            redirect('user');
        }
    }
    
    public function login()
    {
        $this->load->helper('form');
        $this->load->library('form_validation');
        $this->load->helper('url');
        $data['title'] = 'Login';
        
        $this->form_validation->set_rules('email', 'e-mail', 'required');
        $this->form_validation->set_rules('password', 'password', 'required');
        
        
        if ($this->form_validation->run() === FALSE) {
            $this->load->view('templates/header', $data);
            $this->load->view('user/login');
            $this->load->view('templates/footer');
        } else if($this->user_model->validate() === TRUE) {
            redirect('/');
        }
        else {
            $this->load->view('message');
        }
        
    }
    
    
}
